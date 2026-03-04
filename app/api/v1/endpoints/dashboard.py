from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ....db.session import get_db
from ....crud import dashboard as crud_dashboard

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get comprehensive dashboard summary with statistics and recent activity"""
    return crud_dashboard.get_dashboard_summary(db)

@router.get("/quick-stats")
def get_quick_stats(db: Session = Depends(get_db)):
    """Get quick statistics for dashboard overview"""
    return crud_dashboard.get_quick_stats(db)

@router.get("/trends")
def get_dashboard_trends(db: Session = Depends(get_db)):
    """Get monthly trends for dashboard charts"""
    summary = crud_dashboard.get_dashboard_summary(db)
    return {
        "monthlyTrends": summary["monthlyTrends"],
        "lastUpdated": summary["lastUpdated"]
    }
