"""Recommendation router - handles personalized product recommendations."""

import json
import logging
import os
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import cache_get, cache_set, get_db
from app.models import Interaction, Product, User

router = APIRouter()
logger = logging.getLogger(__name__)


def _resolve_model_dir() -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    env_value = os.getenv("MODEL_PATH", "").strip()

    candidates = []
    if env_value:
        candidates.append(Path(env_value).expanduser())
    candidates.extend(
        [
            repo_root / "ml" / "models",
            repo_root / "ml",
            Path("/app/ml"),
        ]
    )

    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else (repo_root / candidate)
        if resolved.exists():
            return resolved.resolve()

    return (repo_root / "ml" / "models").resolve()


MODEL_DIR = _resolve_model_dir()
logger.info("Using ML model directory: %s", MODEL_DIR)

_model = None
_vectorizer = None
_product_similarity = None
_user_item_matrix = None


def _load_models():
    global _model, _vectorizer, _product_similarity, _user_item_matrix

    model_path = MODEL_DIR / "model.pkl"
    vectorizer_path = MODEL_DIR / "vectorizer.pkl"
    similarity_path = MODEL_DIR / "product_similarity.npy"
    matrix_path = MODEL_DIR / "user_item_matrix.npy"

    if not all(path.exists() for path in [model_path, vectorizer_path, similarity_path, matrix_path]):
        logger.warning(
            "ML model artifacts missing in %s. Falling back to deterministic popularity recommendations.",
            MODEL_DIR,
        )
        return

    try:
        _model = joblib.load(model_path)
        _vectorizer = joblib.load(vectorizer_path)
        _product_similarity = np.load(similarity_path)
        _user_item_matrix = np.load(matrix_path)
    except Exception as exc:  # pragma: no cover - depends on artifact integrity
        logger.warning("Could not load ML model artifacts: %s", exc)


_load_models()


def _fallback_products(db: Session, top_n: int, user_id: Optional[int] = None):
    query = db.query(Product).filter(Product.is_active == True)
    if user_id is not None:
        query = query.outerjoin(Interaction, Product.id == Interaction.product_id)
        query = query.group_by(Product.id).order_by(func.count(Interaction.id).desc(), Product.created_at.desc(), Product.id.asc())
    else:
        query = query.order_by(Product.created_at.desc(), Product.id.asc())

    products = query.limit(top_n).all()
    return [
        {"product_id": product.id, "score": 0.75, "rank": index + 1, "product": product}
        for index, product in enumerate(products)
    ]


def get_collaborative_recommendations(user_id: int, db: Session, top_n: int = 10):
    """Collaborative recommendations, with a deterministic popularity fallback."""
    products = db.query(Product).filter(Product.is_active == True).order_by(Product.id).all()
    users = db.query(User).order_by(User.id).all()
    user_idx_map = {user.id: index for index, user in enumerate(users)}
    product_idx = user_idx_map.get(user_id)

    if _model is not None and _user_item_matrix is not None and product_idx is not None and product_idx < _user_item_matrix.shape[0]:
        from scipy.sparse import csr_matrix

        sparse = csr_matrix(_user_item_matrix)
        scores = _model.transform(sparse[[product_idx]])[0]
        top_indices = np.argsort(-scores)[:top_n]
        recs = []
        for rank, pidx in enumerate(top_indices):
            if pidx < len(products):
                recs.append({
                    "product_id": products[pidx].id,
                    "score": float(scores[pidx]),
                    "rank": rank + 1,
                    "product": products[pidx],
                })
        if recs:
            return recs

    return _fallback_products(db, top_n, user_id=user_id)


def get_content_based_recommendations(product_id: int, db: Session, top_n: int = 5):
    """Content-based recommendations, falling back by category and recency."""
    products = db.query(Product).filter(Product.is_active == True).order_by(Product.id).all()
    product_id_to_idx = {product.id: index for index, product in enumerate(products)}

    if _product_similarity is not None and product_id in product_id_to_idx:
        idx = product_id_to_idx[product_id]
        if idx < _product_similarity.shape[0]:
            scores = _product_similarity[idx]
            top_indices = np.argsort(-scores)
            recs = []
            for pidx in top_indices:
                if pidx != idx and pidx < len(products) and len(recs) < top_n:
                    recs.append({
                        "product_id": products[pidx].id,
                        "score": float(scores[pidx]),
                        "rank": len(recs) + 1,
                        "product": products[pidx],
                    })
            if recs:
                return recs

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return []
    similar = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id,
        Product.is_active == True,
    ).order_by(Product.created_at.desc(), Product.id.asc()).limit(top_n).all()
    return [{"product_id": p.id, "score": 0.7, "rank": index + 1, "product": p} for index, p in enumerate(similar)]


def _product_to_dict(p):
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "category": p.category,
        "price": p.price,
        "image_url": p.image_url,
        "tags": p.tags,
        "stock_quantity": p.stock_quantity,
    }


@router.get("/recommend/{user_id}")
async def get_recommendations(
    user_id: int,
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Get personalized recommendations for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    cache_key = f"recommendations:user={user_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    recommendations = get_collaborative_recommendations(user_id, db, top_n)
    serialized = [
        {
            "product_id": rec["product_id"],
            "score": rec["score"],
            "rank": rec["rank"],
            "product": _product_to_dict(rec["product"]),
        }
        for rec in recommendations
    ]

    result = {
        "user_id": user_id,
        "recommendations": serialized,
        "model_version": "fallback-popular" if _model is None else "v1.0-hybrid-nmf",
        "generated_at": str(func.now()),
    }

    cache_set(cache_key, json.dumps(result, default=str), ttl=300)
    return result


@router.get("/similar/{product_id}")
async def get_similar_products(
    product_id: int,
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """Get similar products based on the current product catalog."""
    cache_key = f"similar:product={product_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    similar = get_content_based_recommendations(product_id, db, top_n)
    serialized = [
        {
            "product_id": rec["product_id"],
            "score": rec["score"],
            "rank": rec["rank"],
            "product": _product_to_dict(rec["product"]),
        }
        for rec in similar
    ]

    result = {
        "product_id": product_id,
        "similar_products": serialized,
        "model_version": "fallback-catalog" if _product_similarity is None else "v1.0-content-tfidf",
    }

    cache_set(cache_key, json.dumps(result, default=str), ttl=600)
    return result


@router.post("/track_click")
async def track_click(
    user_id: int,
    product_id: int,
    interaction_type: str = "click",
    db: Session = Depends(get_db),
):
    """Track user interaction with a product."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.add(
        Interaction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
        )
    )
    db.commit()
    return {"message": "Interaction tracked successfully"}
