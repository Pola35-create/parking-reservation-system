from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.parking_spot import ParkingSpot
from app.models.person import Person
from app.models.reservation import Reservation

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Parking Reservation System API"}