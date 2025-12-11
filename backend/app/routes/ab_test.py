"""A/B testing router - handles experiment tracking and analytics."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models import ABTest, User
from app.schemas import ABTestEvent, ABTestMetrics, ABTestResults

router = APIRouter()

@router.post("/track")
async def track_ab_event(
    event: ABTestEvent,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Track an A/B test event (impression, click, or purchase).
    Used to measure variant performance.
    """
    # Create AB test record
    ab_event = ABTest(
        user_id=user_id,
        variant=event.variant,
        product_id=event.product_id,
        action=event.action,
        session_id=event.session_id
    )
    db.add(ab_event)
    db.commit()
    
    return {"message": "Event tracked successfully"}

@router.get("/results", response_model=ABTestResults)
async def get_ab_test_results(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get A/B test results and metrics.
    Calculates CTR and conversion rates for each variant.
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get metrics for each variant
    variants = db.query(ABTest.variant).distinct().all()
    variant_metrics = []
    
    for (variant,) in variants:
        # Count impressions, clicks, and purchases
        impressions = db.query(ABTest).filter(
            ABTest.variant == variant,
            ABTest.action == "impression",
            ABTest.timestamp >= start_date
        ).count()
        
        clicks = db.query(ABTest).filter(
            ABTest.variant == variant,
            ABTest.action == "click",
            ABTest.timestamp >= start_date
        ).count()
        
        purchases = db.query(ABTest).filter(
            ABTest.variant == variant,
            ABTest.action == "purchase",
            ABTest.timestamp >= start_date
        ).count()
        
        # Calculate rates
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        conversion_rate = (purchases / clicks * 100) if clicks > 0 else 0
        
        variant_metrics.append(ABTestMetrics(
            variant=variant,
            impressions=impressions,
            clicks=clicks,
            purchases=purchases,
            ctr=round(ctr, 2),
            conversion_rate=round(conversion_rate, 2)
        ))
    
    # Determine winner (highest CTR)
    winner = None
    if variant_metrics:
        winner = max(variant_metrics, key=lambda x: x.ctr).variant
    
    return ABTestResults(
        variants=variant_metrics,
        winner=winner,
        confidence=None  # TODO: Calculate statistical significance
    )

@router.get("/user-cohort/{user_id}")
async def get_user_cohort(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get the A/B test cohort assignment for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return {
        "user_id": user_id,
        "cohort": user.cohort,
        "variant": user.cohort  # Same as cohort for now
    }

@router.post("/assign-cohort/{user_id}")
async def assign_cohort(
    user_id: int,
    cohort: str = Query(..., regex="^[A-Z]$"),
    db: Session = Depends(get_db)
):
    """Manually assign a user to a specific A/B test cohort."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    user.cohort = cohort
    db.commit()
    
    return {
        "user_id": user_id,
        "cohort": cohort,
        "message": "Cohort assigned successfully"
    }
