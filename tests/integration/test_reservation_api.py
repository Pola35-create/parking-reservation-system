from app.enums.parking_spot_type import ParkingSpotType
from app.enums.reservation_status import ReservationStatus


def create_person(client, **overrides):
    payload = {
        "name": "John",
        "email": "john@example.com",
        "can_use_electric": False,
        "can_use_accessible": False,
        "can_use_dedicated": False,
    }

    payload.update(overrides)

    response = client.post("/persons", json=payload)

    assert response.status_code == 201

    return response.json()


def create_parking_spot(
    client,
    spot_name="A001",
    spot_type=ParkingSpotType.STANDARD.value,
):
    response = client.post(
        "/parking-spots",
        json={
            "spot_name": spot_name,
            "type": spot_type,
        },
    )

    assert response.status_code == 201

    return response.json()


def create_reservation(
    client,
    person_id,
    parking_spot_id,
    start="2026-08-14T10:00:00",
    end="2026-08-14T12:00:00",
):
    return client.post(
        "/reservations",
        json={
            "person_id": person_id,
            "parking_spot_id": parking_spot_id,
            "start_time": start,
            "end_time": end,
        },
    )


def test_create_reservation(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    response = create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["person_id"] == person["id"]
    assert data["parking_spot_id"] == spot["id"]
    assert data["status"] == ReservationStatus.RESERVED.value


def test_overlapping_reservation_is_rejected(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    first = create_reservation(
        client,
        person["id"],
        spot["id"],
        "2026-08-14T10:00:00",
        "2026-08-14T12:00:00",
    )

    second = create_reservation(
        client,
        person["id"],
        spot["id"],
        "2026-08-14T11:00:00",
        "2026-08-14T13:00:00",
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_adjacent_reservations_are_accepted(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    first = create_reservation(
        client,
        person["id"],
        spot["id"],
        "2026-08-14T10:00:00",
        "2026-08-14T12:00:00",
    )

    second = create_reservation(
        client,
        person["id"],
        spot["id"],
        "2026-08-14T12:00:00",
        "2026-08-14T14:00:00",
    )

    assert first.status_code == 201
    assert second.status_code == 201


def test_nonexistent_person_is_rejected(client):
    spot = create_parking_spot(client)

    response = create_reservation(
        client,
        999,
        spot["id"],
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"


def test_nonexistent_parking_spot_is_rejected(client):
    person = create_person(client)

    response = create_reservation(
        client,
        person["id"],
        999,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Parking spot not found"


def test_invalid_time_interval_is_rejected(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    response = create_reservation(
        client,
        person["id"],
        spot["id"],
        "2026-08-14T14:00:00",
        "2026-08-14T10:00:00",
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Start time must be before end time"
    )


def test_cancel_reservation(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    reservation = create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    reservation_id = reservation.json()["id"]

    response = client.delete(
        f"/reservations/{reservation_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reservation_id
    assert data["status"] == ReservationStatus.CANCELLED.value


def test_cancelled_reservation_remains_in_database(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    reservation = create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    reservation_id = reservation.json()["id"]

    delete_response = client.delete(
        f"/reservations/{reservation_id}"
    )

    assert delete_response.status_code == 200

    get_response = client.get("/reservations")

    assert get_response.status_code == 200

    reservations = get_response.json()

    assert len(reservations) == 1
    assert reservations[0]["id"] == reservation_id
    assert reservations[0]["status"] == ReservationStatus.CANCELLED.value


def test_cancelled_reservation_does_not_block_new_reservation(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    first = create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    first_id = first.json()["id"]

    cancel_response = client.delete(
        f"/reservations/{first_id}"
    )

    assert cancel_response.status_code == 200

    second = create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    assert second.status_code == 201


def test_cancel_nonexistent_reservation(client):
    response = client.delete("/reservations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"


def test_get_reservations(client):
    person = create_person(client)
    spot = create_parking_spot(client)

    create_reservation(
        client,
        person["id"],
        spot["id"],
    )

    response = client.get("/reservations")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_reservations_for_parking_spot(client):
    person = create_person(client)

    spot_a = create_parking_spot(
        client,
        spot_name="A001",
    )

    spot_b = create_parking_spot(
        client,
        spot_name="A002",
    )

    create_reservation(
        client,
        person["id"],
        spot_a["id"],
    )

    create_reservation(
        client,
        person["id"],
        spot_b["id"],
        "2026-08-14T14:00:00",
        "2026-08-14T16:00:00",
    )

    response = client.get(
        f"/parking-spots/{spot_a['id']}/reservations"
    )

    assert response.status_code == 200

    reservations = response.json()

    assert len(reservations) == 1
    assert reservations[0]["parking_spot_id"] == spot_a["id"]


def test_get_reservations_for_nonexistent_parking_spot(client):
    response = client.get(
        "/parking-spots/999/reservations"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Parking spot not found"