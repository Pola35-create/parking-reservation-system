from datetime import datetime
import pytest
from fastapi import HTTPException
from app.enums.parking_spot_type import ParkingSpotType
from app.enums.reservation_status import ReservationStatus
from app.models.person import Person
from app.models.parking_spot import ParkingSpot
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.services.reservation_service import create_reservation, cancel_reservation


def create_person(
    db_session,
    person_id=1,
    can_use_electric=False,
    can_use_accessible=False,
    can_use_dedicated=False,
):
    person = Person(
        id=person_id,
        name=f"Person {person_id}",
        email=f"person{person_id}@example.com",
        can_use_electric=can_use_electric,
        can_use_accessible=can_use_accessible,
        can_use_dedicated=can_use_dedicated,
    )

    db_session.add(person)
    db_session.commit()

    return person


def create_parking_spot(
    db_session,
    spot_id=1,
    spot_type=ParkingSpotType.STANDARD,
):
    spot = ParkingSpot(
        id=spot_id,
        spot_name=f"A{spot_id:03d}",
        type=spot_type,
    )

    db_session.add(spot)
    db_session.commit()

    return spot


def create_reservation_data(
    person_id=1,
    parking_spot_id=1,
    start_hour=10,
    end_hour=12,
):
    return ReservationCreate(
        person_id=person_id,
        parking_spot_id=parking_spot_id,
        start_time=datetime(2026, 8, 14, start_hour, 0),
        end_time=datetime(2026, 8, 14, end_hour, 0),
    )


def test_create_valid_reservation(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    reservation_data = create_reservation_data()

    reservation = create_reservation(
        db_session,
        reservation_data,
    )

    assert reservation.id is not None
    assert reservation.person_id == 1
    assert reservation.parking_spot_id == 1
    assert reservation.status == ReservationStatus.RESERVED
    assert reservation.start_time == reservation_data.start_time
    assert reservation.end_time == reservation_data.end_time


def test_overlapping_reservation_is_rejected(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    first = create_reservation(
        db_session,
        create_reservation_data(
            start_hour=10,
            end_hour=12,
        ),
    )

    assert first.status == ReservationStatus.RESERVED

    with pytest.raises(HTTPException) as exc:
        create_reservation(
            db_session,
            create_reservation_data(
                start_hour=11,
                end_hour=13,
            ),
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == (
        "Parking spot is already reserved during this time"
    )


def test_adjacent_reservation_is_accepted(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    first = create_reservation(
        db_session,
        create_reservation_data(
            start_hour=10,
            end_hour=12,
        ),
    )

    second = create_reservation(
        db_session,
        create_reservation_data(
            start_hour=12,
            end_hour=14,
        ),
    )

    assert first.status == ReservationStatus.RESERVED
    assert second.status == ReservationStatus.RESERVED


def test_same_start_and_end_is_rejected(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    reservation_data = create_reservation_data(
        start_hour=10,
        end_hour=10,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(db_session, reservation_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Start time must be before end time"


def test_start_after_end_is_rejected(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    reservation_data = create_reservation_data(
        start_hour=14,
        end_hour=12,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(db_session, reservation_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Start time must be before end time"


def test_different_parking_spot_same_time_is_accepted(db_session):
    create_person(db_session)
    create_parking_spot(db_session, spot_id=1)
    create_parking_spot(db_session, spot_id=2)

    first = create_reservation(
        db_session,
        create_reservation_data(
            parking_spot_id=1,
            start_hour=10,
            end_hour=12,
        ),
    )

    second = create_reservation(
        db_session,
        create_reservation_data(
            parking_spot_id=2,
            start_hour=10,
            end_hour=12,
        ),
    )

    assert first.id != second.id
    assert first.parking_spot_id == 1
    assert second.parking_spot_id == 2


def test_nonexistent_person_is_rejected(db_session):
    create_parking_spot(db_session)

    reservation_data = create_reservation_data(
        person_id=999,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(db_session, reservation_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Person not found"


def test_nonexistent_parking_spot_is_rejected(db_session):
    create_person(db_session)

    reservation_data = create_reservation_data(
        parking_spot_id=999,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(db_session, reservation_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Parking spot not found"


def test_unauthorized_electric_person_is_rejected(db_session):
    create_person(
        db_session,
        can_use_electric=False,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.ELECTRIC,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(
            db_session,
            create_reservation_data(),
        )

    assert exc.value.status_code == 403


def test_authorized_electric_person_is_accepted(db_session):
    create_person(
        db_session,
        can_use_electric=True,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.ELECTRIC,
    )

    reservation = create_reservation(
        db_session,
        create_reservation_data(),
    )

    assert reservation.status == ReservationStatus.RESERVED


def test_unauthorized_accessible_person_is_rejected(db_session):
    create_person(
        db_session,
        can_use_accessible=False,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.ACCESSIBLE,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(
            db_session,
            create_reservation_data(),
        )

    assert exc.value.status_code == 403


def test_authorized_accessible_person_is_accepted(db_session):
    create_person(
        db_session,
        can_use_accessible=True,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.ACCESSIBLE,
    )

    reservation = create_reservation(
        db_session,
        create_reservation_data(),
    )

    assert reservation.status == ReservationStatus.RESERVED


def test_unauthorized_dedicated_person_is_rejected(db_session):
    create_person(
        db_session,
        can_use_dedicated=False,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.DEDICATED,
    )

    with pytest.raises(HTTPException) as exc:
        create_reservation(
            db_session,
            create_reservation_data(),
        )

    assert exc.value.status_code == 403


def test_authorized_dedicated_person_is_accepted(db_session):
    create_person(
        db_session,
        can_use_dedicated=True,
    )
    create_parking_spot(
        db_session,
        spot_type=ParkingSpotType.DEDICATED,
    )

    reservation = create_reservation(
        db_session,
        create_reservation_data(),
    )

    assert reservation.status == ReservationStatus.RESERVED


def test_cancel_reservation(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    reservation = create_reservation(
        db_session,
        create_reservation_data(),
    )

    cancelled = cancel_reservation(
        db_session,
        reservation.id,
    )

    assert cancelled.status == ReservationStatus.CANCELLED

    stored = db_session.get(Reservation, reservation.id)

    assert stored.status == ReservationStatus.CANCELLED


def test_cancelled_reservation_does_not_block_new_reservation(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    first = create_reservation(
        db_session,
        create_reservation_data(
            start_hour=10,
            end_hour=12,
        ),
    )

    cancel_reservation(
        db_session,
        first.id,
    )

    second = create_reservation(
        db_session,
        create_reservation_data(
            start_hour=10,
            end_hour=12,
        ),
    )

    assert second.id != first.id
    assert second.status == ReservationStatus.RESERVED


def test_cancel_nonexistent_reservation_is_rejected(db_session):
    with pytest.raises(HTTPException) as exc:
        cancel_reservation(
            db_session,
            999,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Reservation not found"


def test_cancel_already_cancelled_reservation_is_rejected(db_session):
    create_person(db_session)
    create_parking_spot(db_session)

    reservation = create_reservation(
        db_session,
        create_reservation_data(),
    )

    cancel_reservation(
        db_session,
        reservation.id,
    )

    with pytest.raises(HTTPException) as exc:
        cancel_reservation(
            db_session,
            reservation.id,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Reservation is already cancelled"