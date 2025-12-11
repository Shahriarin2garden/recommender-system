"""
SQLAlchemy ORM models for the recommender system.
Defines database schema for users, products, interactions, and recommendations.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """User model for authentication and personalization."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    cohort = Column(String, default="A", index=True)  # For A/B testing
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    interactions = relationship("Interaction", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class Product(Base):
    """Product model for e-commerce items."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # Comma-separated tags
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    interactions = relationship("Interaction", back_populates="product")
    recommendations = relationship("Recommendation", back_populates="product")

class Interaction(Base):
    """User-product interaction model (views, clicks, purchases, ratings)."""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    interaction_type = Column(String, nullable=False)  # view, click, purchase, rating
    rating = Column(Float, nullable=True)  # Optional rating (1-5)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String, nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON string for additional data (renamed from metadata)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")

class Recommendation(Base):
    """Cached recommendations for users."""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)  # Recommendation confidence score
    model_version = Column(String, nullable=False)  # Track which model generated this
    rank = Column(Integer, nullable=False)  # Ranking position (1-N)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    product = relationship("Product", back_populates="recommendations")

class ABTest(Base):
    """A/B test tracking and metrics."""
    __tablename__ = "ab_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    variant = Column(String, nullable=False)  # A, B, C, etc.
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    action = Column(String, nullable=False)  # impression, click, purchase
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_id = Column(String, nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON string for additional metrics (renamed from metadata)
