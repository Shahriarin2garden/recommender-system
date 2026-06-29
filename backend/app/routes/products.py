"""Products router - handles product listing, details, and search."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database import get_db, cache_get, cache_set
from app.models import Product
from app.schemas import ProductResponse, ProductCreate, ProductUpdate

router = APIRouter()


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "image_url": product.image_url,
        "tags": product.tags,
        "stock_quantity": product.stock_quantity,
        "is_active": product.is_active,
        "created_at": str(product.created_at) if product.created_at else None,
    }

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of products with pagination and optional category filter.
    Results are cached in Redis for 5 minutes.
    """
    # Build cache key
    cache_key = f"products:v2:skip={skip}:limit={limit}:category={category}"
    
    # Try cache first
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Query database
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    
    products = query.offset(skip).limit(limit).all()
    
    # Cache results
    cache_set(cache_key, json.dumps([serialize_product(p) for p in products]))
    
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific product."""
    # Try cache first
    cache_key = f"product:v2:{product_id}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Query database
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    
    # Cache result
    cache_set(cache_key, json.dumps(serialize_product(product)))
    
    return product

@router.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product (admin only)."""
    # TODO: Add admin authentication check
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.get("/categories/")
async def get_categories(db: Session = Depends(get_db)):
    """Get list of all product categories."""
    cache_key = "categories:all"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)
    
    categories = db.query(Product.category).distinct().all()
    result = [cat[0] for cat in categories]
    
    cache_set(cache_key, json.dumps(result), ttl=3600)  # Cache for 1 hour
    
    return result

@router.get("/products/search/")
async def search_products(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    """Search products by name or description."""
    products = db.query(Product).filter(
        (Product.name.ilike(f"%{q}%")) | (Product.description.ilike(f"%{q}%"))
    ).filter(Product.is_active == True).limit(20).all()
    
    return products
