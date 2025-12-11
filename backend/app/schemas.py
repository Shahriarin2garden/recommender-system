"""
Pydantic schemas for request/response validation.
Provides type safety and automatic validation for API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    cohort: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# ============================================================================
# Product Schemas
# ============================================================================

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    tags: Optional[str] = None

class ProductCreate(ProductBase):
    stock_quantity: int = Field(default=0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    tags: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    stock_quantity: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Interaction Schemas
# ============================================================================

class InteractionBase(BaseModel):
    product_id: int
    interaction_type: str = Field(..., pattern="^(view|click|purchase|rating)$")
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    session_id: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionResponse(InteractionBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Recommendation Schemas
# ============================================================================

class RecommendationResponse(BaseModel):
    product_id: int
    score: float
    rank: int
    product: ProductResponse
    
    class Config:
        from_attributes = True

class RecommendationList(BaseModel):
    user_id: int
    recommendations: List[RecommendationResponse]
    model_version: str
    generated_at: datetime

# ============================================================================
# A/B Test Schemas
# ============================================================================

class ABTestEvent(BaseModel):
    variant: str = Field(..., pattern="^[A-Z]$")
    product_id: Optional[int] = None
    action: str = Field(..., pattern="^(impression|click|purchase)$")
    session_id: Optional[str] = None

class ABTestMetrics(BaseModel):
    variant: str
    impressions: int
    clicks: int
    purchases: int
    ctr: float  # Click-through rate
    conversion_rate: float
    
class ABTestResults(BaseModel):
    variants: List[ABTestMetrics]
    winner: Optional[str] = None
    confidence: Optional[float] = None

# ============================================================================
# General Response Schemas
# ============================================================================

class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int
