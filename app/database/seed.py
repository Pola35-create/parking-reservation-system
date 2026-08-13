from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.enums.parking_spot_type import ParkingSpotType
from app.models.parking_spot import ParkingSpot
from app.models.person import Person

# Seed the database with initial data
def seed_database():
    db: Session = SessionLocal()

    try:
        # Check whether the database already contains data
        if db.query(ParkingSpot).first() is not None:
            return # Database already contains seed data

        # Create initial parking spots
        parking_spots = [
            ParkingSpot(spot_name="A001", type=ParkingSpotType.STANDARD),
            ParkingSpot(spot_name="A002", type=ParkingSpotType.STANDARD),
            ParkingSpot(spot_name="B001", type=ParkingSpotType.ACCESSIBLE),
            ParkingSpot(spot_name="B002", type=ParkingSpotType.ACCESSIBLE),
            ParkingSpot(spot_name="C001", type=ParkingSpotType.ELECTRIC),
            ParkingSpot(spot_name="C002", type=ParkingSpotType.ELECTRIC),
            ParkingSpot(spot_name="D001", type=ParkingSpotType.DEDICATED),
            ParkingSpot(spot_name="D002", type=ParkingSpotType.DEDICATED)
        ]

        # Create initial people
        people = [
            Person(name="Alice", email="alice@example.com"),
            Person(name="Bob", email="bob@example.com"),
            Person(name="Charlie", email="charlie@example.com"),
            Person(name="David", email="david@example.com"),
            Person(name="Eve", email="eve@example.com")
        ]

        # Add and commit the initial data to the database
        db.add_all(parking_spots)
        db.add_all(people)
        db.commit()

    # Handle any exceptions that occur during the seeding process
    except Exception:
        db.rollback()
        raise

    # Close the database session
    finally:
        db.close()