from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.parking_spot import ParkingSpot
from app.schemas.parking_spot import ParkingSpotCreate, ParkingSpotResponse


router = APIRouter(
    prefix="/parking-spots",
    tags=["Parking Spots"]
)


@router.post(
    "",
    response_model=ParkingSpotResponse,
    status_code=201
)
def create_parking_spot(
    parking_spot: ParkingSpotCreate,
    db: Session = Depends(get_db)
):
    existing_spot = db.query(ParkingSpot).filter(
        ParkingSpot.spot_name == parking_spot.spot_name
    ).first()

    if existing_spot:
        raise HTTPException(
            status_code=409,
            detail="Parking spot with this name already exists"
        )

    new_parking_spot = ParkingSpot(
        spot_name=parking_spot.spot_name,
        type=parking_spot.type
    )

    db.add(new_parking_spot)
    db.commit()
    db.refresh(new_parking_spot)

    return new_parking_spot


@router.get(
    "",
    response_model=list[ParkingSpotResponse]
)
def get_parking_spots(
    db: Session = Depends(get_db)
):
    return db.query(ParkingSpot).all()