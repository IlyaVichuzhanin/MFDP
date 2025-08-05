from fastapi.testclient import TestClient





def test_home_request(client: TestClient):
    response=client.get("/test")
    assert response.status_code==200
    assert response.json() == {"message": "success"}



def test_get_user_balance(client: TestClient):
    user_id = {"id": "773e3742-c9ae-4f10-85d8-da3d0d3490b6"}
    response = client.post("/balance/get_user_balance", json=user_id)

    assert response.status_code==200
    assert response.json()=={"message": "Get balance successfuly"}


def test_increase_user_balance(client: TestClient):
    user_id = {"id": "773e3742-c9ae-4f10-85d8-da3d0d3490b6"
               
               }
    response = client.post("/balance/increase_user_balance", json=user_id)

    assert response.status_code==200
    assert response.json()=={"message": "Get balance successfuly"}