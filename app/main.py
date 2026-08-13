from fastapi import FastAPI
from app.api import person
from app.api import parking_spot
from app.api import reservation

# Initialize FastAPI app
app = FastAPI(
    title="Parking Reservation System API",
)

app.include_router(parking_spot.router)
app.include_router(person.router)
app.include_router(reservation.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Parking Reservation System API"}