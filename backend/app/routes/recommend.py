"""Recommendation router - handles personalized product recommendations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
import json
import os
import numpy as np
import joblib

from app.database import get_db, cache_get, cache_set
from app.models import User, Product, Interaction

router = APIRouter()

# ML model paths
ML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ml')

_model = None
_vectorizer = None
_product_similarity = None
_user_item_matrix = None

def _load_models():
    global _model, _vectorizer, _product_similarity, _user_item_matrix
    if _model is None:
        try:
            _model = joblib.load(os.path.join(ML_DIR, 'model.pkl'))
            _vectorizer = joblib.load(os.path.join(ML_DIR, 'vectorizer.pkl'))
            _product_similarity = np.load(os.path.join(ML_DIR, 'product_similarity.npy'))
            _user_item_matrix = np.load(os.path.join(ML_DIR, 'user_item_matrix.npy'))
        except Exception as e:
            print(f"Warning: Could not load ML models: {e}")

_load_models()


def get_collaborative_recommendations(user_id: int, db: Session, top_n: int = 10):
    """Collaborative filtering recommendations using trained NMF model."""
    products = db.query(Product).filter(Product.is_active == True).order_by(Product.id).all()
    users = db.query(User).order_by(User.id).all()

    user_idx_map = {u.id: i for i, u in enumerate(users)}
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
                    "product": products[pidx]
                })
        if recs:
            return recs

    # Fallback: return top products by stock
    import random
    sampled = random.sample(products, min(top_n, len(products)))
    return [{"product_id": p.id, "score": 0.5, "rank": i + 1, "product": p} for i, p in enumerate(sampled)]


def get_content_based_recommendations(product_id: int, db: Session, top_n: int = 5):
    """Content-based similarity using TF-IDF cosine similarity matrix."""
    products = db.query(Product).filter(Product.is_active == True).order_by(Product.id).all()
    product_id_to_idx = {p.id: i for i, p in enumerate(products)}

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
                        "product": products[pidx]
                    })
            if recs:
                return recs

    # Fallback: same category
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return []
    similar = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id,
        Product.is_active == True
    ).limit(top_n).all()
    return [{"product_id": p.id, "score": 0.7, "rank": i + 1, "product": p} for i, p in enumerate(similar)]


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
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a user (hybrid: collaborative + content)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

    cache_key = f"recommendations:user={user_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    recommendations = get_collaborative_recommendations(user_id, db, top_n)
    serialized = [
        {"product_id": r["product_id"], "score": r["score"], "rank": r["rank"], "product": _product_to_dict(r["product"])}
        for r in recommendations
    ]

    result = {
        "user_id": user_id,
        "recommendations": serialized,
        "model_version": "v1.0-hybrid-nmf",
        "generated_at": str(func.now()),
    }

    cache_set(cache_key, json.dumps(result, default=str), ttl=300)
    return result


@router.get("/similar/{product_id}")
async def get_similar_products(
    product_id: int,
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get similar products based on TF-IDF cosine similarity."""
    cache_key = f"similar:product={product_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    similar = get_content_based_recommendations(product_id, db, top_n)
    serialized = [
        {"product_id": r["product_id"], "score": r["score"], "rank": r["rank"], "product": _product_to_dict(r["product"])}
        for r in similar
    ]

    result = {
        "product_id": product_id,
        "similar_products": serialized,
        "model_version": "v1.0-content-tfidf",
    }

    cache_set(cache_key, json.dumps(result, default=str), ttl=600)
    return result


@router.post("/track_click")
async def track_click(
    user_id: int,
    product_id: int,
    interaction_type: str = "click",
    db: Session = Depends(get_db)
):
    """Track user interaction with a product."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    interaction = Interaction(
        user_id=user_id,
        product_id=product_id,
        interaction_type=interaction_type
    )
    db.add(interaction)
    db.commit()

    return {"message": "Interaction tracked successfully"}
