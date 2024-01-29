import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from prep_phase import prep_user, prep_products
from PIL import Image
from io import BytesIO
from product.models import Category

import logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_get_products(client):
    prep_user(client)
    prep_products(client, k=10)
    
    #GET products by category
    get_products_by_category = client.get(reverse("products_by_category", kwargs={"category": "food"}))
    assert get_products_by_category.status_code == 200
    assert len(get_products_by_category.data) == 5
    
    #GET products
    pagination = f"?limit=5"
    get_products = client.get(f"{reverse('products') + pagination}")
    assert get_products.status_code == 200
    assert len(get_products.data["results"]) == 5

    product_1 = get_products.data["results"][0]
    product_2 = get_products.data["results"][1]
    #GET product by id
    get_product_by_id = client.get(reverse("product", kwargs={"pk": product_1["id"]}))
    assert get_product_by_id.status_code == 200
    assert get_product_by_id.data["id"] == product_1["id"]
    assert get_product_by_id.data["name"] == product_1["name"]
    assert get_product_by_id.data["price"] == product_1["price"]

    #UPDATE product
    update_data = {
        "name": "Orange shirt",
        "sku": "WW2906AS",
        "description": "Lorem ipsum",
        "price": 330000,
    }
    update_product = client.put(reverse("product", kwargs={"pk": product_1["id"]}), data=update_data, format="multipart")
    assert update_product.status_code == 200
    assert update_product.data["name"] == update_data["name"]
    assert update_product.data["description"] == update_data["description"]
    
    #DELETE product
    del_product = client.delete(reverse("product", kwargs={"pk": product_1["id"]}))
    assert del_product.status_code == 204
    assert del_product.data == None
    
    #DELETE product without permission
    prep_user(client, is_user2=True)
    del_product = client.delete(reverse("product", kwargs={"pk": product_2["id"]}))
    assert del_product.status_code == 403
    
@pytest.mark.django_db
def test_create_product(client):
    prep_user(client)
    Category.objects.create(
        name="t-shirt",
        description="This is a t-shirt category"
        )
    #Create product
    size = (400, 400)
    storage = BytesIO()
    img = Image.new("RGB", size)
    img.save(storage, "JPEG")
    storage.seek(0)
    file = SimpleUploadedFile(
        name="test_img.jpg",
        content=storage.getvalue(),
        content_type="image/jpeg"
    )
    
    data = {
            "name": "test product",
            "sku": "WW2906AS",
            "description": "description",
            "price": 199000,
            "quantity": 20,
            "category": "t-shirt",
            "images": file,
        }
    
    create_product = client.post(reverse("products"), data = data, format="multipart")
    assert create_product.status_code == 201
    assert create_product.data["name"] == data["name"]