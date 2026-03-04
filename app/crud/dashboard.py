from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from ..models.all_models import Donation, Inquiry, Project, News, PortalUser, Event, Resource, Multimedia
from typing import Dict, Any, List

def get_dashboard_summary(db: Session) -> Dict[str, Any]:
    """Get comprehensive dashboard summary with statistics and recent activity"""
    
    # Get current date and month start (start of day)
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 1. Financial Statistics
    total_donations = db.query(func.sum(Donation.amount)).filter(Donation.status == "completed").scalar() or 0
    donations_this_month = db.query(func.sum(Donation.amount)).filter(
        Donation.status == "completed",
        Donation.created_at >= month_start
    ).scalar() or 0
    donations_last_month = db.query(func.sum(Donation.amount)).filter(
        Donation.status == "completed",
        Donation.created_at >= (month_start - timedelta(days=32)),
        Donation.created_at < month_start
    ).scalar() or 0
    
    # Calculate donation growth
    donation_growth = 0
    if donations_last_month > 0:
        donation_growth = ((donations_this_month - donations_last_month) / donations_last_month) * 100
    
    # 2. Project Statistics
    active_projects = db.query(Project).filter(Project.status == "Active").count()
    completed_projects = db.query(Project).filter(Project.status == "Completed").count()
    total_projects = db.query(Project).count()
    
    # 3. User Statistics
    total_users = db.query(PortalUser).filter(PortalUser.is_active == True).count()
    admin_users = db.query(PortalUser).filter(PortalUser.role == "admin", PortalUser.is_active == True).count()
    staff_users = db.query(PortalUser).filter(PortalUser.role == "staff", PortalUser.is_active == True).count()
    
    # 4. Content Statistics
    published_news = db.query(News).filter(News.published_date <= datetime.now()).count()
    total_events = db.query(Event).count()
    upcoming_events = db.query(Event).filter(Event.start_date >= datetime.now()).count()
    total_resources = db.query(Resource).count()
    total_multimedia = db.query(Multimedia).count()
    
    # 5. Engagement Statistics
    unread_inquiries = db.query(Inquiry).filter(Inquiry.status == "Unread").count()
    total_inquiries = db.query(Inquiry).count()
    pending_inquiries = db.query(Inquiry).filter(Inquiry.status == "Unread").count()
    
    # 7. Recent Activities (more comprehensive)
    activities = []
    
    # Recent donations (last 5)
    recent_donations = db.query(Donation).order_by(desc(Donation.created_at)).limit(5).all()
    for donation in recent_donations:
        activities.append({
            "type": "donation",
            "text": f"Donation of ${donation.amount} from {donation.donor}",
            "time": donation.created_at.isoformat(),
            "status": donation.status,
            "metadata": {
                "email": donation.email,
                "method": donation.method,
                "frequency": donation.frequency
            }
        })
    
    # Recent inquiries (last 5)
    recent_inquiries = db.query(Inquiry).order_by(desc(Inquiry.created_at)).limit(5).all()
    for inquiry in recent_inquiries:
        activities.append({
            "type": "inquiry",
            "text": f"{inquiry.type.capitalize()} inquiry from {inquiry.name}",
            "time": inquiry.created_at.isoformat(),
            "status": inquiry.status,
            "metadata": {
                "email": inquiry.email,
                "subject": inquiry.subject
            }
        })
    
    # Recent user registrations (last 3)
    recent_users = db.query(PortalUser).order_by(desc(PortalUser.created_at)).limit(3).all()
    for user in recent_users:
        activities.append({
            "type": "user",
            "text": f"New {user.role} user registered: {user.name}",
            "time": user.created_at.isoformat(),
            "status": "active" if user.is_active else "inactive",
            "metadata": {
                "email": user.email,
                "role": user.role
            }
        })
    
    # Recent news publications (last 3)
    recent_news = db.query(News).order_by(desc(News.published_date)).limit(3).all()
    for news in recent_news:
        activities.append({
            "type": "news",
            "text": f"News article published: {news.title.get('en', 'Untitled')[:50]}...",
            "time": news.published_date.isoformat(),
            "status": "published",
            "metadata": {
                "author": news.author,
                "category": news.category
            }
        })
    
    # Sort all activities by time (most recent first)
    activities.sort(key=lambda x: x["time"], reverse=True)
    
    # 8. Monthly donation trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        month_start = (now - timedelta(days=30*i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_donations = db.query(func.sum(Donation.amount)).filter(
            Donation.status == "completed",
            Donation.created_at >= month_start,
            Donation.created_at <= month_end
        ).scalar() or 0
        
        month_inquiries = db.query(Inquiry).filter(
            Inquiry.created_at >= month_start,
            Inquiry.created_at <= month_end
        ).count()
        
        monthly_trends.append({
            "month": month_start.strftime("%b"),
            "donations": float(month_donations),  # Already in dollars
            "inquiries": month_inquiries,
            "timestamp": month_start.isoformat()
        })
    
    # Reverse to show oldest to newest
    monthly_trends.reverse()
    
    return {
        "stats": {
            "totalDonations": f"${total_donations}",
            "donationsThisMonth": f"${donations_this_month}",
            "donationsLastMonth": f"${donations_last_month}",
            "donationGrowth": f"{donation_growth:+.1f}%",
            "activeProjects": active_projects,
            "completedProjects": completed_projects,
            "totalProjects": total_projects,
            "pendingTasks": unread_inquiries,
            "totalUsers": total_users,
            "adminUsers": admin_users,
            "staffUsers": staff_users,
            "publishedNews": published_news,
            "upcomingEvents": upcoming_events,
            "totalEvents": total_events,
            "totalResources": total_resources,
            "totalMultimedia": total_multimedia,
            "totalInquiries": total_inquiries
        },
        "recentActivity": activities[:10],  # Return top 10 activities
        "monthlyTrends": monthly_trends,
        "lastUpdated": datetime.now().isoformat()
    }

def get_quick_stats(db: Session) -> Dict[str, Any]:
    """Get quick stats for dashboard overview"""
    return {
        "totalDonations": db.query(func.sum(Donation.amount)).filter(Donation.status == "completed").scalar() or 0,
        "activeProjects": db.query(Project).filter(Project.status == "Active").count(),
        "unreadInquiries": db.query(Inquiry).filter(Inquiry.status == "Unread").count(),
        "totalUsers": db.query(PortalUser).filter(PortalUser.is_active == True).count(),
        "publishedNews": db.query(News).filter(News.published_date <= datetime.now()).count(),
        "upcomingEvents": db.query(Event).filter(Event.start_date >= datetime.now()).count()
    }
