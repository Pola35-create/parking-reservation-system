from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.reservation_service import create_reservation, cancel_reservation


router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=201
)
def create(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    return create_reservation(db, reservation)


@router.delete(
    "/{reservation_id}",
    response_model=ReservationResponse,
)
def cancel(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    return cancel_reservation(db, reservation_id)

@router.get(
    "",
    response_model=list[ReservationResponse]
)
def get_reservations(
    db: Session = Depends(get_db)
):
    return db.query(Reservation).all()