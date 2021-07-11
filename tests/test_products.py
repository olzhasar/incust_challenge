import os
from io import BytesIO

import pytest
from api.models import Product


class TestProductCreate:
    url = "/products"

    @pytest.fixture
    def product_data(self, product_list):
        return {
            "product_list_id": product_list.id,
            "sku": "12345",
            "name": "Product 1",
            "image": (BytesIO(b"product.jpg"), "product.jpg"),
        }

    def test_ok(self, client, user, as_user, product_data, product_list):
        response = as_user.post(
            self.url,
            data=product_data,
            content_type="multipart/form-data",
        )

        assert response.status_code == 201

        product = Product.query.filter_by(
            product_list_id=product_list.id,
            sku="12345",
            name="Product 1",
        ).one_or_none()

        assert product.image == "product.jpg"
        assert os.path.exists(product.image_filepath)

        assert response.json == {
            "id": product.id,
            "product_list_id": product_list.id,
            "sku": product.sku,
            "name": product.name,
            "prices": [],
            "image": "/media/product.jpg",
        }

    def test_not_unique_sku(self, as_user, product_data, product):
        product_data["sku"] = product.sku

        response = as_user.post(
            self.url,
            data=product_data,
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        assert (
            response.json["detail"]
            == "Each product must have a unique SKU inside product list"
        )

    def test_unauthorized(self, client, product_data):
        response = client.post(
            self.url,
            data=product_data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 401

    def test_other_users_product_list(self, as_other_user, product_data):
        response = as_other_user.post(
            self.url,
            data=product_data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 400


class TestProductDelete:
    url = "/products/{}"

    def test_ok(self, as_user, product):
        response = as_user.delete(self.url.format(product.id))

        assert response.status_code == 204

    def test_unexisting(self, as_user):
        response = as_user.delete(self.url.format(999))

        assert response.status_code == 404

    def test_other_user(self, product, as_other_user):
        response = as_other_user.delete(self.url.format(product.id))

        assert response.status_code == 404

    def test_unauthorized(self, client, product):
        response = client.delete(self.url.format(product.id))

        assert response.status_code == 401
