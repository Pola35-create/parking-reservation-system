from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.enums.parking_spot_type import ParkingSpotType
from app.enums.reservation_status import ReservationStatus
from app.models.person import Person
from app.models.parking_spot import ParkingSpot
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

def create_reservation(
        db: Session,
        reservation: ReservationCreate
):
    # 1. Check if the person exists
    person = db.query(Person).filter(
        Person.id == reservation.person_id
        ).first()
    if not person:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    # 2. Check if the parking spot exists
    parking_spot = db.query(ParkingSpot).filter(
        ParkingSpot.id == reservation.parking_spot_id
        ).first()
    if not parking_spot:
        raise HTTPException(
            status_code=404,
            detail="Parking spot not found"
        )

    # 3. Check that start time is before end time
    if reservation.start_time >= reservation.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be before end time"
        )

    # 4. Check whether the person is eligible
    if parking_spot.type.value == ParkingSpotType.ELECTRIC.value and not person.can_use_electric:
        raise HTTPException(
            status_code=403,
            detail="Person is not eligible to reserve electric parking spots"
        )

    elif parking_spot.type.value == ParkingSpotType.ACCESSIBLE.value and not person.can_use_accessible:
        raise HTTPException(
            status_code=403,
            detail="Person is not eligible to reserve accessible parking spots"
        )

    elif parking_spot.type.value == ParkingSpotType.DEDICATED.value and not person.can_use_dedicated:
        raise HTTPException(
            status_code=403,
            detail="Person is not eligible to reserve dedicated parking spots"
        )

    # 5. Check for overlapping reservations
    overlapping_reservation = db.query(Reservation).filter(
        Reservation.parking_spot_id == reservation.parking_spot_id,
        Reservation.status == ReservationStatus.RESERVED,
        Reservation.start_time < reservation.end_time,
        Reservation.end_time > reservation.start_time
    ).first()

    if overlapping_reservation:
        raise HTTPException(
            status_code=409,
            detail="Parking spot is already reserved during this time"
        )

    # 6. Create a new reservation
    new_reservation = Reservation(
        person_id=reservation.person_id,
        parking_spot_id=reservation.parking_spot_id,
        start_time=reservation.start_time,
        end_time=reservation.end_time,
        status=ReservationStatus.RESERVED
    )

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation

def cancel_reservation(
        db: Session,
        reservation_id: int
):
    # Find the reservation
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    # Check if the reservation is already cancelled
    if reservation.status == ReservationStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Reservation is already cancelled"
        )

    # Change status to CANCELLED
    reservation.status = ReservationStatus.CANCELLED

    db.commit()
    db.refresh(reservation)

    return reservation