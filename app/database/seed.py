from sqlalchemy.orm import Session
from app.database.database import Base, engine, SessionLocal
from app.enums.parking_spot_type import ParkingSpotType
from app.models.parking_spot import ParkingSpot
from app.models.person import Person
from app.models.reservation import Reservation

# Seed the database with initial data
def seed_database():
    # Create database tables and session
    Base.metadata.create_all(bind=engine)
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
            Person(name="Alice", email="alice@example.com", can_use_electric=True, can_use_accessible=False, can_use_dedicated=False),
            Person(name="Bob", email="bob@example.com", can_use_electric=False, can_use_accessible=False, can_use_dedicated=True),
            Person(name="Charlie", email="charlie@example.com", can_use_electric=False, can_use_accessible=False, can_use_dedicated=False),
            Person(name="David", email="david@example.com", can_use_electric=False, can_use_accessible=True, can_use_dedicated=False),
            Person(name="Eve", email="eve@example.com", can_use_electric=True, can_use_accessible=False, can_use_dedicated=False)
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

# Run the seed_database function if this script is executed directly
if __name__ == "__main__":
    seed_database()