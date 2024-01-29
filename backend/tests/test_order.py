import pytest
from django.urls import reverse
from prep_phase import prep_user, prep_products
from user.models import PaymentType

import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_create_order(client):
    #Prep phase
    prep_user(client)
    prep_products(client, k=10)
    
    address_data ={
        "name": "House address",
        "city": "Ho Chi Minh City",
        "address": "123 street, some district",
        "phone_number": "0102030405"
    }
    create_res = client.post(reverse("addresses"), data=address_data, format="json")
    assert create_res.status_code == 201
    
    payment_type = PaymentType.objects.create(name="paypal")
    payment = {
        "payment_type": "paypal",
        "provider": "visa",
        "account_number": "090909090",
        "expiry_date": "12-24"
    }
    
    create_payment = client.post(reverse("payments"), data=payment, format="json")
    assert create_payment.status_code == 201

    get_products = client.get(reverse("products"))
    product_1 = get_products.data[6]
    product_2 = get_products.data[8]
    
    pd_list = {
        "products":[
            {
                "product_id": product_1["id"],
                "quantity": 3,
            },
            {
                "product_id": product_2["id"],
                "quantity": 2,
            },
        ],
        "address": create_res.data["id"],
        "payment": create_payment.data["id"],
    }
    
    #Main test
    create_order = client.post(reverse("orders"), data=pd_list, format="json")
    assert create_order.status_code == 201
    assert create_order.data["status"] == "processing"
    assert create_order.data["created_by"] == create_payment.data["created_by"]

    get_order = client.get(reverse("orders"))
    assert get_order.status_code == 200
    assert len(get_order.data) == 1