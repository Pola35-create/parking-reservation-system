from app.enums.parking_spot_type import ParkingSpotType


def test_create_parking_spot(client):
    response = client.post(
        "/parking-spots",
        json={
            "spot_name": "A001",
            "type": ParkingSpotType.STANDARD.value,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["spot_name"] == "A001"
    assert data["type"] == ParkingSpotType.STANDARD.value


def test_duplicate_parking_spot_is_rejected(client):
    payload = {
        "spot_name": "A001",
        "type": ParkingSpotType.STANDARD.value,
    }

    first = client.post("/parking-spots", json=payload)
    second = client.post("/parking-spots", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == (
        "Parking spot with this name already exists"
    )


def test_get_parking_spots(client):
    client.post(
        "/parking-spots",
        json={
            "spot_name": "A001",
            "type": ParkingSpotType.STANDARD.value,
        },
    )

    response = client.get("/parking-spots")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["spot_name"] == "A001"