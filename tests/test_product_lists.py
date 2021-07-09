import pytest
from api.models import ProductList


class TestProductListCreate:
    url = "/product_lists"

    @pytest.fixture
    def product_1_data(self):
        return {
            "sku": "12345",
            "name": "Product 1",
            "image_url": "https://cool.product/image.jpg",
            "prices": [
                {
                    "currency_code": "USD",
                    "value": 500,
                },
                {
                    "currency_code": "GBP",
                    "value": 300,
                },
            ],
        }

    @pytest.fixture
    def product_2_data(self):
        return {
            "sku": "34567",
            "name": "Product 2",
            "image_url": "https://cool.product/image.jpg",
            "prices": [
                {
                    "currency_code": "JPY",
                    "value": 250,
                },
                {
                    "currency_code": "EUR",
                    "value": 150,
                },
            ],
        }

    @pytest.fixture
    def products_data(self, product_1_data, product_2_data):
        return [product_1_data, product_2_data]

    def test_ok(self, client, user_1, as_user_1, products_data):
        response = as_user_1.post(
            self.url,
            json={
                "name": "My list",
                "products": products_data,
            },
        )

        assert response.status_code == 201

        product_list = ProductList.query.filter_by(user_id=user_1.id).one_or_none()
        assert product_list.name == "My list"

        for product, data in zip(product_list.products, products_data):
            assert product.sku == data["sku"]
            assert product.name == data["name"]
            assert product.image_url == data["image_url"]

            for price, price_data in zip(product.prices, data["prices"]):
                assert price.value == price_data["value"]
                assert price.currency_code == price_data["currency_code"]

    def test_skus_not_unique(self, client, user_1, as_user_1, product_1_data):
        response = as_user_1.post(
            self.url,
            json={
                "name": "not_unique_list",
                "products": [product_1_data, product_1_data],
            },
        )

        assert response.status_code == 400
        assert (
            response.json["detail"]
            == "Each product must have a unique SKU inside product list"
        )

        assert not ProductList.query.filter_by(
            user_id=user_1.id, name="not_unique_list"
        ).one_or_none()

    def test_prices_not_unique(self, client, user_1, as_user_1, product_1_data):
        product_1_data["prices"] = [
            {
                "currency_code": "USD",
                "value": 100,
            },
            {
                "currency_code": "USD",
                "value": 200,
            },
        ]

        response = as_user_1.post(
            self.url,
            json={
                "name": "not_unique_list",
                "products": [product_1_data],
            },
        )

        assert response.status_code == 400
        assert (
            response.json["detail"]
            == "Only one price value is allowed for each currency code"
        )

        assert not ProductList.query.filter_by(
            user_id=user_1.id, name="not_unique_list"
        ).one_or_none()

    def test_invalid_request(self, client, user_1, as_user_1):
        response = as_user_1.post(
            self.url,
            json={
                "name": "invalid_list",
                "products": [{}],
            },
        )

        assert response.status_code == 400