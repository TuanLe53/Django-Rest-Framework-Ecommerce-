from auth_api.models import CustomUser
from django.urls import reverse
from product.models import Category

def prep_user(client, is_user2: bool = False):
    if is_user2:
        user_payload = {
            "email": "test_2gmail.com",
            "password": "pw123456"
        }
    else:
        user_payload ={
            "email": "test@gmail.com",
            "password": "pw123456"
        }
    user = CustomUser.objects.create(email=user_payload["email"])
    user.set_password(user_payload["password"])
    user.save()
    
    res = client.post(reverse("login"), data=user_payload, format="json")
    access_token = res.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    
def prep_products(client, k:int):
    Category.objects.create(
        name="t-shirt",
        description="This is a t-shirt category"
        )
    
    for i in range(k):
        product = {
            "name": f"t-shirt {i}",
            "sku": "WW2906AS",
            "description": "description",
            "price": 199000 + i,
            "quantity": i,
            "category": "t-shirt"
        }
        client.post(reverse("products"), data = product, format="multipart")

    Category.objects.create(
        name="food",
        description="this is a food category"
    )
    for _ in range(5):
        product = {
            "name": f"food {_}",
            "sku": "WW2906AS",
            "description": "description",
            "price": 199000 + _,
            "quantity": _,
            "category": "food"
        }
        client.post(reverse("products"), data = product, format="multipart")