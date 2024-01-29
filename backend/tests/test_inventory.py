import pytest
from django.urls import reverse
from prep_phase import prep_user, prep_products

@pytest.mark.django_db
def test_inventory(client):
    prep_user(client)
    prep_products(client, k=5)
    
    get_products = client.get(reverse("products"))
    product = get_products.data[4]
    assert product is not None
    
    inventory_id, _ = product["inventory"].split(" ")
    
    new_quantity = {
        "quantity": 10
    }
    
    update_quantity = client.put(reverse("inventory", kwargs={"pk": inventory_id[:len(inventory_id)-1]}), data=new_quantity, format="json")
    assert update_quantity.status_code == 200
    assert update_quantity.data["quantity"] == new_quantity["quantity"]