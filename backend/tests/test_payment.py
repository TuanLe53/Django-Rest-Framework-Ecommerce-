import pytest
from django.urls import reverse
from prep_phase import prep_user
from user.models import PaymentType

import logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_create_payment(client):
    prep_user(client)
    payment_type = PaymentType.objects.create(name="paypal")
    
    payment = {
        "payment_type": "paypal",
        "provider": "visa",
        "account_number": "090909090",
        "expiry_date": "12-24"
    }
    
    create_payment = client.post(reverse("payments"), data=payment, format="json")
    assert create_payment.status_code == 201
    assert create_payment.data["account_number"] == payment["account_number"]
    
    get_payments = client.get(reverse("payments"))
    assert get_payments.status_code == 200
    assert len(get_payments.data) == 1
    logger.info(f'{get_payments.data}')