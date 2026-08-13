def test_create_person(client):
    response = client.post(
        "/persons",
        json={
            "name": "John",
            "email": "john@example.com",
            "can_use_electric": True,
            "can_use_accessible": False,
            "can_use_dedicated": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "John"
    assert data["email"] == "john@example.com"
    assert data["can_use_electric"] is True


def test_duplicate_person_email_is_rejected(client):
    payload = {
        "name": "John",
        "email": "john@example.com",
        "can_use_electric": False,
        "can_use_accessible": False,
        "can_use_dedicated": False,
    }

    first = client.post("/persons", json=payload)
    second = client.post("/persons", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "This email already exists"


def test_get_persons(client):
    client.post(
        "/persons",
        json={
            "name": "John",
            "email": "john@example.com",
            "can_use_electric": False,
            "can_use_accessible": False,
            "can_use_dedicated": False,
        },
    )

    response = client.get("/persons")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "john@example.com"