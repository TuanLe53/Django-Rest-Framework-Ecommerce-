import pytest
from django.urls import reverse
from prep_phase import prep_products, prep_user

@pytest.mark.django_db
def test_cart(client):
    prep_user(client)
    prep_products(client, k=5)
    
    get_products = client.get(reverse("products"))
    product = get_products.data[4]
    product_2 = get_products.data[3]
    
    cart_item = {
        "product": product["id"],
        "quantity": 2
    }
    cart_item_2 = {
        "product": product_2["id"],
        "quantity": 1
    }
    
    add_to_cart = client.post(reverse("cart"), data=cart_item, format="json")
    assert add_to_cart.status_code == 201
    
    add_to_cart = client.post(reverse("cart"), data=cart_item_2, format="json")
    assert add_to_cart.status_code == 201
    
    get_cart_items = client.get(reverse("cart"))
    assert get_cart_items.status_code == 200
    assert get_cart_items.data is not None
    assert len(get_cart_items.data) == 2
    
    #REMOVE item from cart
    rm_item = get_cart_items.data[0]["id"]
    rm_from_cart = client.delete(reverse("cart_item", kwargs={"pk": rm_item}))
    assert rm_from_cart.status_code == 204
    assert rm_from_cart.data == None