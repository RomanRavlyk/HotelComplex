from http.client import responses

from fastapi.testclient import TestClient
from sqlalchemy.orm.loading import instances

from app.main import app
import pytest
from app.database import get_session
from app.config import get_test_session, init_test_db, drop_test_db

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_test_db()
    yield
    drop_test_db()


def test_create_hotel():
    hotel_data = {"hotel_name": "TestHotel"}
    response = client.post("/hotel/create_hotel/", json=hotel_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["hotel_name"] == hotel_data["hotel_name"]

    hotel_data = {"hotel_name": "TestHotel2"}
    response = client.post("/hotel/create_hotel/", json=hotel_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["hotel_name"] == hotel_data["hotel_name"]

def test_get_hotel():
    hotel_data = {"hotel_id": "0", "hotel_name": "TestHotel"}
    response = client.get("/hotel/get_hotel/?id=0&hotel_name=TestHotel")
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data["hotel_name"] == hotel_data["hotel_name"]

def test_get_all_hotels():
    response = client.get("/hotel/hotels/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for hotel in response_data:
        assert "id" in hotel
        assert "hotel_name" in hotel

        assert isinstance(hotel["id"], int)

        assert hotel["hotel_name"] != ""

def test_update_hotel():
    hotel_data = {"id": 2, "hotel_name": "HotelTest2"}
    response=client.put("/hotel/update_hotel/", json=hotel_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["hotel_name"] == hotel_data["hotel_name"]

def test_delete_hotel():
    hotel_data = {"id": 2, "hotel_name": "HotelTest2"}
    response = client.request("DELETE", "/hotel/delete_hotel/", json=hotel_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Hotel deleted"

def test_get_hotel_stats():
    response = client.get("/hotel/get_hotel_stats/?hotel_id=1")
    assert response.status_code == 200
    response_data = response.json()
    print(f"response_data: {response_data}")
    assert isinstance(response_data, dict)

def test_hotel_stats_created():
    hotel_data = {"hotel_name": "TestHotelWithStats"}
    response = client.post("/hotel/create_hotel/", json=hotel_data)
    assert response.status_code == 200

    hotel_id = response.json()["id"]
    response_stats = client.get(f"/hotel/get_hotel_stats/?hotel_id={hotel_id}")
    assert response_stats.status_code == 200
    assert "expenses" in response_stats.json()
    assert "hotel_id" in response_stats.json()
    assert "income" in response_stats.json()

def test_create_hotel_amenity():
    hotel_amenity_data1 = {
        "amenity_name": "SPA",
        "amenity_cost": 70,
        "plus_adults": 2,
        "plus_children": 1,
        "hotel_id": 1
    }

    hotel_amenity_data2 = {
        "amenity_name": "WIFI",
        "amenity_cost": 90,
        "plus_adults": 0,
        "plus_children": 0,
        "hotel_id": 1
    }

    response = client.post("/hotel/create_hotel_amenity/", json=hotel_amenity_data1)
    response_data = response.json()
    assert response.status_code == 200
    assert "id" in response_data
    assert response_data["hotel_id"] == hotel_amenity_data1["hotel_id"]
    assert response_data["amenity_name"] == "SPA"
    assert response_data["amenity_cost"] == 70
    assert response_data["plus_adults"] == 2
    assert response_data["plus_children"] == 1

    response = client.post("/hotel/create_hotel_amenity/", json=hotel_amenity_data2)
    response_data = response.json()
    assert response.status_code == 200
    assert "id" in response_data
    assert response_data["hotel_id"] == hotel_amenity_data2["hotel_id"]
    assert response_data["amenity_name"] == "WIFI"
    assert response_data["amenity_cost"] == 90
    assert response_data["plus_adults"] == 0
    assert response_data["plus_children"] == 0

def test_get_by_id_amenity():
    hotel_amenity_data1 = {
        "amenity_name": "SPA",
        "amenity_cost": 70,
        "plus_adults": 2,
        "plus_children": 1,
        "hotel_id": 1
    }

    response = client.get(f"/hotel/get_amenity_by_id/?amenity_id=1&hotel_id=1")
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["hotel_id"] == 1
    assert response_data["amenity_name"] == "SPA"
    assert response_data["amenity_cost"] == 70
    assert response_data["plus_adults"] == 2
    assert response_data["plus_children"] == 1

def test_change_hotel_amenity():
    hotel_amenity_data2 = {
        "amenity": {
            "id": 2,
            "amenity_name": "Kitchen",
            "amenity_cost": 170,
            "plus_adults": 2,
            "plus_children": 1,
        },
        "hotel_id": {
            "id": 1
        }
    }

    response = client.put("/hotel/change_hotel_amenity/", json=hotel_amenity_data2)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["hotel_id"] == 1
    assert response_data["amenity_name"] == "Kitchen"
    assert response_data["amenity_cost"] == 170
    assert response_data["plus_adults"] == 2
    assert response_data["plus_children"] == 1

def test_delete_hotel_amenity():
    amenity_data = {"amenity_id": 2,
  "hotel": {
    "id": 1
  }}
    response = client.request("DELETE", "/hotel/delete_amenity/", json=amenity_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Amenity deleted"

def test_cottage_create():
    cottage_data1 = {
      "cottage_name": "TestCottage",
      "hotel_id": 1,
      "cost_per_day": 500,
      "cottage_type": "Lux",
      "adults": 8,
      "childs": 4
    }

    cottage_data2 = {
        "cottage_name": "TestCottage2",
        "hotel_id": 1,
        "cost_per_day": 200,
        "cottage_type": "Economic",
        "adults": 4,
        "childs": 2
    }

    response1 = client.post("/cottage/create_cottage/", json=cottage_data1)
    assert response1.status_code == 200
    response_data = response1.json()
    assert "id" in response_data
    assert response_data["cottage_name"] == cottage_data1["cottage_name"]
    assert response_data["cost_per_day"] == cottage_data1["cost_per_day"]
    assert response_data["cottage_type"] == cottage_data1["cottage_type"]
    assert response_data["adults"] == cottage_data1["adults"]
    assert response_data["childs"] == cottage_data1["childs"]
    assert response_data["hotel_id"] == cottage_data1["hotel_id"]

    response2 = client.post("/cottage/create_cottage/", json=cottage_data2)
    assert response2.status_code == 200
    response_data = response2.json()
    assert "id" in response_data
    assert response_data["cottage_name"] == cottage_data2["cottage_name"]
    assert response_data["cost_per_day"] == cottage_data2["cost_per_day"]
    assert response_data["cottage_type"] == cottage_data2["cottage_type"]
    assert response_data["adults"] == cottage_data2["adults"]
    assert response_data["childs"] == cottage_data2["childs"]
    assert response_data["hotel_id"] == cottage_data2["hotel_id"]

def test_cottage_get():
    cottage_data1 = {
      "cottage_name": "TestCottage",
      "hotel_id": 1,
      "cost_per_day": 500,
      "cottage_type": "Lux",
      "adults": 8,
      "childs": 4
    }
    response = client.get("/cottage/get_cottage/?cottage_name=TestCottage")
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["cottage_name"] == cottage_data1["cottage_name"]
    assert response_data["cost_per_day"] == cottage_data1["cost_per_day"]
    assert response_data["cottage_type"] == cottage_data1["cottage_type"]
    assert response_data["adults"] == cottage_data1["adults"]
    assert response_data["childs"] == cottage_data1["childs"]
    assert response_data["hotel_id"] == cottage_data1["hotel_id"]

def test_get_cottages():
    cottage_data1 = {
      "cottage_name": "TestCottage",
      "hotel_id": 1,
      "cost_per_day": 500,
      "cottage_type": "Lux",
      "adults": 8,
      "childs": 4
    }

    response = client.get("/cottage/get_cottages/")
    response_data = response.json()

    for cottage in response_data:
        assert "id" in cottage
        assert cottage["cottage_name"] == cottage_data1["cottage_name"]
        assert cottage["cost_per_day"] == cottage_data1["cost_per_day"]
        assert cottage["cottage_type"] == cottage_data1["cottage_type"]
        assert cottage["adults"] == cottage_data1["adults"]
        assert cottage["childs"] == cottage_data1["childs"]
        assert cottage["hotel_id"] == cottage_data1["hotel_id"]
        break

def test_change_cottage():
    cottage_data2 = {
        "id": 1,
        "cottage_name": "CottageTest2",
        "hotel_id": 1,
        "cost_per_day": 700,
        "cottage_type": "Lux",
        "adults": 12,
        "childs": 6
    }

    response = client.put("/cottage/change_cottage/", json=cottage_data2)
    response_data = response.json()
    assert "id" in response_data
    assert response_data["cottage_name"] == cottage_data2["cottage_name"]
    assert response_data["cost_per_day"] == cottage_data2["cost_per_day"]
    assert response_data["cottage_type"] == cottage_data2["cottage_type"]
    assert response_data["adults"] == cottage_data2["adults"]
    assert response_data["childs"] == cottage_data2["childs"]
    assert response_data["hotel_id"] == cottage_data2["hotel_id"]

def test_get_cottage_by_type():
    cottage_type: str = "Lux"
    response = client.get("/cottage/get_cottage_by_type/?cottage_type=Lux")
    response_data = response.json()
    for cottage in response_data:
        assert "id" in cottage
        assert cottage["cottage_type"] == cottage_type

def test_delete_cottage():
    cottage_data = {"id": 1}
    response = client.request("DELETE", "/cottage/delete_cottage/", json=cottage_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Cottage successfully deleted"


def test_get_hotel_cottages():
    response = client.get("/hotel/get_hotel_cottages/?id=1")
    response_data = response.json()
    for cottage in response_data:
        assert "id" in cottage

def test_get_cottage_available_amenities():
    response = client.get("/cottage/get_available_amenities/?cottage_id=2")
    assert response.status_code == 200
    response_data = response.json()
    for amenity in response_data:
        assert "amenity_name" in amenity

def test_add_amenity_to_cottage():
    hotel_amenity_data1 = {
        "amenity_name": "SPA",
        "amenity_cost": 70,
        "plus_adults": 2,
        "plus_children": 1,
        "hotel_id": 1
    }

    response = client.post("/cottage/add_amenity_to_cottage/?cottage_id=2&amenity_id=1")
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["amenity_name"] == "SPA"
    assert response_data["amenity_cost"] == 70
    assert response_data["plus_adults"] == 2
    assert response_data["plus_children"] == 1


def test_get_cottage_amenities():
    response = client.get("/cottage/get_available_amenities/?cottage_id=2")
    assert response.status_code == 200
    response_data = response.json()
    for amenity in response_data:
        assert "id" in amenity

def test_get_cottage_amenity_by_id():
    response = client.get("/cottage/get_cottage_amenity/?cottage_id=2&amenity_id=1")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == 1

def test_delete_cottage_amenity():
    response = client.request("DELETE", "/cottage/delete_cottage_amenity/?amenity_id=1&cottage_id=2")
    response_data = response.json()

    assert response_data["message"] == "Cottage amenity successfully deleted"

def test_user_registration():
    data = {
        "username": "Pasha",
        "password": "12345678"
    }

    response = client.post("/auth/register/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data["user"]
    assert response_data["user"]["username"] == "Pasha"
    assert response_data["message"] == "User registered successfully"

def test_user_login():
    data = {
        "username": "Pasha",
        "password": "12345678"
    }

    response = client.post("/auth/login/", json=data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Logged in"

def test_user_get_me():
    response = client.get("/auth/me/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_id"] == "1"



def test_create_booking():
    data = {
        "user_id": 1,
        "cottage_id": 2,
        "start_date": "2024-11-26T23:17:37.665Z",
        "end_date": "2024-11-27T23:17:37.665Z"
    }

    response = client.post("/booking/create_booking/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_id"] == 1
    assert response_data["cottage_id"] == 2
    assert response_data["start_date"] == "2024-11-26T23:17:37.665000"
    assert response_data["end_date"] == "2024-11-27T23:17:37.665000"

def test_get_user_bookings():
    response = client.get("/booking/get_user_bookings/?user_id=1")
    assert response.status_code == 200
    response_data = response.json()
    for booking in response_data:
        assert "id" in booking
        assert booking["cottage_id"] == 2

def test_check_cottage_availability():
    data={
        "cottage_id": 2,
        "dates": {
            "start_date": "2024-11-28T23:25:39.249Z",
            "end_date": "2024-11-30T23:25:39.249Z"
        }
    }

    response = client.post("/booking/check_availability/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    print(f"response_data: {response_data}")
    assert response_data["cottage_id"] == 2
    assert response_data["available"] == True

def test_check_available_periods():
    response = client.post("/booking/get_available_periods/?cottage_id=2")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["cottage_id"] == 2
    for period in response_data:
        assert period is not None

def test_update_booking():
    data = {
        "id": 1,
        "user_id": 1,
        "cottage_id": 2,
        "start_date": "2024-12-01T23:42:17.334Z",
        "end_date": "2024-12-25T23:42:17.334Z"
    }

    response = client.put("/booking/update_user_booking/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_id"] == 1
    assert response_data["cottage_id"] == 2
    assert response_data["start_date"] == "2024-12-01T23:42:17.334000"
    assert response_data["end_date"] == "2024-12-25T23:42:17.334000"

def test_delete_booking():
    response = client.request("DELETE", "/booking/delete_user_booking/?user_id=1&booking_id=1")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "Successfully deleted"

def test_user_logout():
    response = client.post("/auth/logout/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Logged out"