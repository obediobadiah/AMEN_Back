import sys
import os
from datetime import datetime

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.db.session import SessionLocal, engine, Base
from app.models.all_models import News, Project, Resource, Event, Multimedia, GovernanceMember, LiveStat

def seed_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed News
        if not db.query(News).first():
            news_items = [
                {
                    "title": {"fr": "La Dignité des Êtres Humains au Travail", "en": "The Dignity of Human Beings to Work"},
                    "excerpt": {"fr": "Explorer comment la dignité dans le travail transforme les communautés...", "en": "Exploring how dignity in labor transforms communities and builds self-reliance."},
                    "content": {"fr": "Le travail est plus qu'un simple moyen de survie...", "en": "Work is more than just a means of survival..."},
                    "author": "Jean-Pierre Kabangu",
                    "category": "impact",
                    "reading_time": 5,
                    "thumbnail_url": "/images/news1.jpg",
                    "published_date": datetime(2024, 2, 14)
                },
                {
                    "title": {"fr": "Le Pouvoir des Gens Contre la Pauvreté", "en": "The Power of People Against Poverty"},
                    "excerpt": {"fr": "Les initiatives dirigées par la communauté montrent des résultats remarquables...", "en": "Community-led initiatives are showing remarkable results..."},
                    "content": {"fr": "La pauvreté est souvent perçue comme une force insurmontable...", "en": "Poverty is often seen as an insurmountable force..."},
                    "author": "Marie-Louise Mambo",
                    "category": "field",
                    "reading_time": 4,
                    "thumbnail_url": "/images/news2.jpg",
                    "published_date": datetime(2024, 2, 10)
                },
                {
                    "title": {"fr": "Force motrice hors de la pauvreté", "en": "Driving Force Out of Poverty"},
                    "excerpt": {"fr": "L'éducation reste l'outil le plus efficace...", "en": "Education remains the single most effective tool for breaking the cycle of poverty."},
                    "content": {"fr": "L'éducation est souvent appelée le grand égalisateur...", "en": "Education is often called the great equalizer..."},
                    "author": "Paul Bakenga",
                    "category": "press",
                    "reading_time": 6,
                    "thumbnail_url": "/images/news3.jpg",
                    "published_date": datetime(2024, 1, 28)
                },
                {
                    "title": {"fr": "Techniques d'Agriculture Durable pour les Ménages Ruraux", "en": "Sustainable Agriculture Techniques for Rural Households"},
                    "excerpt": {"fr": "De nouveaux ateliers aident les agriculteurs...", "en": "New workshops help farmers adapt to climate change while increasing yields."},
                    "content": {"fr": "Le changement climatique n'est plus une menace lointaine...", "en": "Climate change is no longer a distant threat..."},
                    "author": "Alice Zola",
                    "category": "field",
                    "reading_time": 7,
                    "thumbnail_url": "/images/hero-projects.jpg",
                    "published_date": datetime(2024, 1, 15)
                }
            ]
            for item in news_items:
                db.add(News(**item))
            print("News seeded!")

        # 2. Seed Projects
        if not db.query(Project).first():
            projects = [
                {
                    "title": {"fr": "Reforestation du Bassin du Congo", "en": "Congo Basin Reforestation"},
                    "description": {"fr": "Restauration de 5 000 hectares de terres forestières...", "en": "Restoring 5,000 hectares of degraded forest land..."},
                    "status": "Active",
                    "location": {"fr": "Province de l'Équateur", "en": "Equateur Province"},
                    "category": "Environnement",
                    "impact_stats": {
                        "fr": {"label": "Arbres plantés", "value": "200,000"},
                        "en": {"label": "Trees planted", "value": "200,000"}
                    },
                    "overview": {"fr": "Cette initiative phare se concentre sur...", "en": "This flagship initiative focuses on..."},
                    "goals": {
                        "fr": ["Planter 1 million d'arbres indigènes d'ici 2026", "Restaurer 5 000 hectares"],
                        "en": ["Plant 1 million trees by 2026", "Restore 5,000 hectares"]
                    },
                    "image_url": "/images/program-nature.jpg"
                },
                {
                    "title": {"fr": "Énergie Solaire pour les Cliniques Rurales", "en": "Solar Power for Rural Clinics"},
                    "description": {"fr": "Installation de systèmes d'énergie solaire...", "en": "Installing off-grid solar energy systems in 10 remote health centers..."},
                    "status": "Active",
                    "location": {"fr": "Région du Kasaï", "en": "Kasaï Region"},
                    "category": "Infrastructure",
                    "impact_stats": {
                        "fr": {"label": "Cliniques équipées", "value": "3/10"},
                        "en": {"label": "Clinics equipped", "value": "3/10"}
                    },
                    "image_url": "/images/news2.jpg"
                }
            ]
            for p in projects:
                db.add(Project(**p))
            print("Projects seeded!")

        # 3. Seed Resources
        if not db.query(Resource).first():
            resources = [
                {
                    "title": {"fr": "Rapport d'Impact Annuel 2023", "en": "Annual Impact Report 2023"},
                    "description": {"fr": "Un aperçu complet de nos activités...", "en": "A comprehensive overview of our activities..."},
                    "file_url": "/files/impact-2023.pdf",
                    "file_size": "4.2 MB",
                    "file_type": "PDF",
                    "category": "annual",
                    "publication_date": datetime(2024, 1, 1)
                },
                {
                    "title": {"fr": "Guide de Gestion Forestière Communautaire", "en": "Community Forest Management Guide"},
                    "description": {"fr": "Un guide technique pour les communautés locales...", "en": "A technical guide for local communities on sustainable forest management..."},
                    "file_url": "/files/forest-guide.pdf",
                    "file_size": "12.5 MB",
                    "file_type": "PDF",
                    "category": "technical",
                    "publication_date": datetime(2023, 11, 15)
                }
            ]
            for r in resources:
                db.add(Resource(**r))
            print("Resources seeded!")

        # 4. Seed Multimedia
        if not db.query(Multimedia).first():
            media = [
                {
                    "title": {"fr": "Sommet sur la Conservation", "en": "Conservation Summit"},
                    "media_url": "/images/gallery1.jpg",
                    "type": "photo",
                    "category": "Nature"
                },
                {
                    "title": {"fr": "Vidéo sur l'Impact", "en": "Impact Video"},
                    "media_url": "https://example.com/video1",
                    "type": "video",
                    "category": "Health"
                }
            ]
            for m in media:
                db.add(Multimedia(**m))
            print("Multimedia seeded!")

        # 5. Seed Events
        if not db.query(Event).first():
            events = [
                {
                    "title": {"fr": "Sommet sur la Conservation du Bassin du Congo 2024", "en": "Congo Basin Conservation Summit 2024"},
                    "description": {"fr": "Un rassemblement d'experts en environnement...", "en": "A gathering of environmental experts..."},
                    "start_date": datetime(2024, 3, 15, 9, 0),
                    "end_date": datetime(2024, 3, 17, 17, 0),
                    "location": {"fr": "Kinshasa, RDC & Virtuel", "en": "Kinshasa, DRC & Virtual"},
                    "status": "Upcoming",
                    "category": "Conference"
                }
            ]
            for e in events:
                db.add(Event(**e))
            print("Events seeded!")

        # 6. Seed Governance Members
        if not db.query(GovernanceMember).first():
            members = [
                {
                    "name": "Jean-Pierre Kabangu",
                    "role": {"fr": "Directeur Général", "en": "General Director"},
                    "bio": {"fr": "Leader expérimenté...", "en": "Experienced leader..."},
                    "organ_id": "dg",
                    "order": 1
                },
                {
                    "name": "Marie-Louise Mambo",
                    "role": {"fr": "Responsable Programmes", "en": "Program Manager"},
                    "bio": {"fr": "Dédiée à l'autonomisation...", "en": "Dedicated to empowerment..."},
                    "organ_id": "dg",
                    "order": 2
                }
            ]
            for m in members:
                db.add(GovernanceMember(**m))
            print("Governance Members seeded!")

        # 7. Seed Live Stats
        if not db.query(LiveStat).first():
            stats = [
                {"label": {"en": "Projects Completed", "fr": "Projets Terminés"}, "value": "90+", "icon_name": "ShieldCheck", "category": "home"},
                {"label": {"en": "Happy Beneficiaries", "fr": "Bénéficiaires Heureux"}, "value": "15k+", "icon_name": "HandHeart", "category": "home"},
                {"label": {"en": "Volunteers", "fr": "Volontaires"}, "value": "350", "icon_name": "Users", "category": "home"},
                {"label": {"en": "Years Active", "fr": "Années d'Activité"}, "value": "12", "icon_name": "Globe", "category": "home"},
                {"label": {"en": "Trees Planted", "fr": "Arbres Plantés"}, "value": "200k+", "icon_name": "Leaf", "category": "impact"},
                {"label": {"en": "Hectares Restored", "fr": "Hectares Restaurés"}, "value": "5,000", "icon_name": "Map", "category": "impact"}
            ]
            for s in stats:
                db.add(LiveStat(**s))
            print("Live Stats seeded!")

        db.commit()
        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
