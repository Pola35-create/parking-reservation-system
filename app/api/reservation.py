from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationResponse


router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=201
)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    new_reservation = Reservation(
        person_id=reservation.person_id,
        parking_spot_id=reservation.parking_spot_id,
        start_time=reservation.start_time,
        end_time=reservation.end_time
    )

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation


@router.get(
    "",
    response_model=list[ReservationResponse]
)
def get_reservations(
    db: Session = Depends(get_db)
):
    return db.query(Reservation).all()