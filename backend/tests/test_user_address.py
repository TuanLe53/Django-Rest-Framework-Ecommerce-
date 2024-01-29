import pytest
from django.urls import reverse
from prep_phase import prep_user

@pytest.mark.django_db
def test_addresses_endpoint(client):
    prep_user(client)
    
    #Create first address
    address_data ={
        "name": "House address",
        "city": "Ho Chi Minh City",
        "address": "123 street, some district",
        "phone_number": "0102030405"
    }
    create_res = client.post(reverse("addresses"), data=address_data, format="json")
    assert create_res.status_code == 201
    assert create_res.data["name"] == address_data["name"]
    assert create_res.data["city"] == address_data["city"]
    assert create_res.data["address"] == address_data["address"]
    assert create_res.data["phone_number"] == address_data["phone_number"]
    
    #Create second address
    create_res = client.post(reverse("addresses"), data=address_data, format="json")
    user_id = create_res.data["created_by"]
    
    #Get Addresses
    get_res = client.get(reverse("addresses"))
    assert get_res.status_code == 200
    assert len(get_res.data) == 2
    assert get_res.data[0]["created_by"] == user_id
    
    #Missing city field
    error_form ={
        "name": "House address",
        "address": "123 street, some district",
        "phone_number": "0102030405"
    }
    create_res_400 = client.post(reverse("addresses"), data=error_form, format="json")
    assert create_res_400.status_code == 400

@pytest.mark.django_db
def test_address_endpoint(client):
    prep_user(client)
    
    address_data ={
        "name": "House address",
        "city": "Ho Chi Minh City",
        "address": "123 street, some district",
        "phone_number": "0102030405"
    }
    create_res = client.post(reverse("addresses"), data=address_data, format="json")
    
    #Get address with id
    address_id = create_res.data["id"]
    get_address = client.get(reverse("address", kwargs={"pk": address_id}))
    assert get_address.status_code == 200
    assert get_address.data["id"] == address_id
    assert get_address.data["phone_number"] == address_data["phone_number"]
    
    #Update address
    update_data = {
        "name": "House address",
        "city": "Ha Noi city",
        "address": "123 street, some district",
        "phone_number": "0102030405"
    }
    update_address = client.put(reverse("address", kwargs={"pk": address_id}), data=update_data)
    assert update_address.status_code == 200
    assert update_address.data["name"] == update_data["name"]
    assert update_address.data["address"] == update_data["address"]
    assert update_address.data["city"] == update_data["city"]
    assert update_address.data["phone_number"] == update_data["phone_number"]
    
    #Delete address
    delete_address = client.delete(reverse("address", kwargs={"pk": address_id}))
    assert delete_address.data == None
    assert delete_address.status_code == 204