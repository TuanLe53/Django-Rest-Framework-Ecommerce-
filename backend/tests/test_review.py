import pytest
from django.urls import reverse
from prep_phase import prep_user, prep_products
import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_review(client):
    prep_user(client)
    prep_products(client, k=5)
    
    get_products = client.get(reverse("products"))
    assert get_products.status_code == 200
    
    product = get_products.data[1]
    product_2 = get_products.data[2]
    
    review = {
        "product": product["id"],
        "rating": 3.5,
        "comment": "This is a comment"
    }
    review_2 = {
        "product": product["id"],
        "rating": 4.0,
        "comment": "This is a comment"
    }
    
    create_review = client.post(reverse("review"), data=review, format="json")
    create_review = client.post(reverse("review"), data=review_2, format="json")
    assert create_review.status_code == 201
    assert create_review.data["comment"] == review["comment"]
    
    get_reviews = client.get(reverse("reviews", kwargs={"pk": product["id"]}))
    assert get_reviews.status_code == 200
    assert len(get_reviews.data) > 0
    
    get_reviews_2 = client.get(reverse("reviews", kwargs={"pk": product_2["id"]}))
    assert get_reviews_2.status_code == 200
    assert len(get_reviews_2.data) == 0
    
    get_product_by_id = client.get(reverse("product", kwargs={"pk": product["id"]}))
    assert get_product_by_id.status_code == 200
    assert get_product_by_id.data["rating"] == "3.8"