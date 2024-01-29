import pytest
from django.urls import reverse
from auth_api.models import CustomUser

payload = {
    "email": "test@gmail.com",
    "password": "pw123456"
    }

@pytest.mark.django_db
def test_register_user(client):
    res =  client.post(reverse("register"), data=payload, format="json")
    assert res.status_code == 201
    assert res.data["email"] == payload["email"]
    
    #Email exists
    res = client.post(reverse("register"), data=payload, format="json")
    assert res.status_code == 400
    
@pytest.mark.django_db
def test_login_user(client):
    user = CustomUser.objects.create(email="test@gmail.com")
    user.set_password("pw123456")
    user.save()
    
    res = client.post(reverse("login"), data=payload, format="json")
    assert res.status_code == 200
    assert res.data["access"] is not None
    assert res.data["refresh"] is not None
    
    #Refresh Token
    token = {
        "refresh": res.data["refresh"]
    }
    get_access_token = client.post(reverse("refresh"), data=token, format="json")
    assert get_access_token.status_code == 200
    assert get_access_token.data["access"] is not None
    
    #User not found
    data = {
        "email": "someemail@gmail.com",
        "password": "thisIsAPW"
    }
    res = client.post(reverse("login"), data=data, format="json")
    assert res.status_code == 401
    
    #Wrong password
    payload["password"] = "wrongPW"
    res = client.post(reverse("login"), data=payload, format="json")
    assert res.status_code == 401