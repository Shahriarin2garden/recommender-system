"""Recommendation router - handles personalized product recommendations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
import json
import random

from app.database import get_db, cache_get, cache_set
from app.models import User, Product, Recommendation, Interaction
from app.schemas import RecommendationResponse, ProductResponse

router = APIRouter()

def get_collaborative_recommendations(user_id: int, db: Session, top_n: int = 10):
    """
    Collaborative filtering recommendations.
    TODO: Replace with actual ML model predictions.
    """
    # Placeholder: Return random products for now
    # In production, this would call the trained ML model
    products = db.query(Product).filter(Product.is_active == True).limit(top_n * 2).all()
    recommendations = random.sample(products, min(top_n, len(products)))
    
    return [
        {
            "product_id": p.id,
            "score": random.uniform(0.5, 1.0),
            "rank": idx + 1,
            "product": p
        }
        for idx, p in enumerate(recommendations)
    ]

def get_content_based_recommendations(product_id: int, db: Session, top_n: int = 5):
    """
    Content-based similarity recommendations.
    TODO: Replace with actual similarity computation using embeddings.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return []
    
    # Placeholder: Return products from same category
    similar_products = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id,
        Product.is_active == True
    ).limit(top_n).all()
    
    return [
        {
            "product_id": p.id,
            "score": random.uniform(0.6, 0.95),
            "rank": idx + 1,
            "product": p
        }
        for idx, p in enumerate(similar_products)
    ]

@router.get("/recommend/{user_id}")
async def get_recommendations(
    user_id: int,
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for a user.
    Uses hybrid approach: collaborative filtering + content-based.
    Results are cached for 5 minutes.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    # Try cache first
    cache_key = f"recommendations:user={user_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Get recommendations (hybrid approach)
    recommendations = get_collaborative_recommendations(user_id, db, top_n)
    
    result = {
        "user_id": user_id,
        "recommendations": recommendations,
        "model_version": "v1.0-hybrid",
        "generated_at": str(db.query(func.now()).scalar())
    }
    
    # Cache results
    cache_set(cache_key, json.dumps(result, default=str), ttl=300)
    
    return result

@router.get("/similar/{product_id}")
async def get_similar_products(
    product_id: int,
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get similar products based on content similarity.
    Useful for "You may also like" sections.
    """
    cache_key = f"similar:product={product_id}:n={top_n}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)
    
    similar = get_content_based_recommendations(product_id, db, top_n)
    
    result = {
        "product_id": product_id,
        "similar_products": similar,
        "model_version": "v1.0-content"
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
    """
    Track user interaction with a product.
    Used for improving recommendations and A/B testing.
    """
    interaction = Interaction(
        user_id=user_id,
        product_id=product_id,
        interaction_type=interaction_type
    )
    db.add(interaction)
    db.commit()
    
    # Invalidate recommendation cache for this user
    cache_key = f"recommendations:user={user_id}:*"
    # TODO: Implement pattern-based cache invalidation
    
    return {"message": "Interaction tracked successfully"}

# Import func for timestamp
from sqlalchemy import func
