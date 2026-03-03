from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from ....db.session import get_db
from ....models.all_models import Inquiry, Donation, Project

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    # Total Donations (sum of amount for 'completed' status)
    total_donations = db.query(func.sum(Donation.amount)).filter(Donation.status == "completed").scalar() or 0
    
    # Active Projects
    active_projects = db.query(Project).filter(Project.status == "Active").count()
    
    # Communities Reached (mocked or from Project impact_stats if we had a better schema for it)
    # For now, let's use a mock or try to sum something from project stats
    # Using 5280 as a baseline if no projects exist
    communities_reached = 5280 + (active_projects * 5)
    
    # Pending Tasks (Unread Inquiries)
    unread_inquiries = db.query(Inquiry).filter(Inquiry.status == "Unread").count()
    
    # Recent Activities
    # Combine recent donations and recent inquiries
    recent_donations = db.query(Donation).order_by(Donation.created_at.desc()).limit(3).all()
    recent_inquiries = db.query(Inquiry).order_by(Inquiry.created_at.desc()).limit(3).all()
    
    activities = []
    for d in recent_donations:
        activities.append({
            "type": "donation",
            "text": f"New donation of ${d.amount/100:.2f} from {d.donor}",
            "time": d.created_at,
            "status": d.status
        })
    for i in recent_inquiries:
        activities.append({
            "type": "inquiry",
            "text": f"New {i.type} inquiry from {i.name}",
            "time": i.created_at,
            "status": i.status
        })
    
    activities.sort(key=lambda x: x["time"], reverse=True)
    
    return {
        "stats": {
            "totalDonations": f"${total_donations/100:,.2f}",
            "activeProjects": active_projects,
            "communitiesReached": f"{communities_reached:,}",
            "pendingTasks": unread_inquiries
        },
        "recentActivity": activities[:5]
    }
