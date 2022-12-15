import requests
from tests.config import API_URL

def test_root():
    response = requests.get(API_URL)
    assert response.status_code == 404


def test_get_owner_by_id(create_owner):
    response = requests.get(f'{API_URL}/owners/{create_owner["id"]}')
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data['email'] == create_owner['email']


def test_create_owner():
    owner_data ={'email': 'new_owner@email.ru', 'password': '2222'}
    response = requests.post(f'{API_URL}/owners/', json=owner_data)
    assert response.status_code == 200
    assert response.json()['email'] == owner_data['email']


def test_patch_owner(create_owner):
    response = requests.patch(f'{API_URL}/owners/{create_owner["id"]}', json={'email': 'patch_owner@email.ru'})
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data['email'] == 'patch_owner@email.ru'


def test_delete_owner(create_owner):
    response = requests.delete(f'{API_URL}/owners/{create_owner["id"]}')
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data['status'] == 'deleted'


def test_get_advertisement_by_id(create_advertisement):
    response = requests.get(f'{API_URL}/ads/{create_advertisement["id"]}')
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert response_data["title"] == create_advertisement["title"]


def test_create_advertisement(create_owner):
    response = requests.post(f'{API_URL}/ads/', auth=(create_owner["email"], '1111'),
                             json={"title": "Шкаф IKEA",
                            "description": "Срочно",
                            "owner_id": create_owner["id"]
    })
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)
    assert 'title' in json_data
    assert json_data['title'] == 'Шкаф IKEA'


def test_patch_advertisemen(create_advertisement):
    response = requests.patch(f'{API_URL}/ads/{create_advertisement["id"]}', auth=(create_advertisement["owner_email"],
                                                                                   '12345'), json={"description": "Новая"})
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)


def test_delete_advertisemen(create_advertisement):
    response = requests.delete(f'{API_URL}/ads/{create_advertisement["id"]}', auth=(create_advertisement["owner_email"],
                                                                                    '1234'))
    assert response.status_code == 200
