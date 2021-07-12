import pytest
from api.models import ProductList, db

from tests import factories


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

    def test_ok(self, client, user, as_user, products_data):
        response = as_user.post(
            self.url,
            json={
                "name": "My list",
            },
        )

        assert response.status_code == 201

        product_list = ProductList.query.filter_by(user_id=user.id).one_or_none()
        assert product_list.name == "My list"


class TestProductListReadOne:
    url = "/product_lists/{}"

    @pytest.fixture
    def products(self, product_list):
        _products = [
            factories.ProductFactory(
                product_list=product_list,
                sku="789",
                name="abc",
            ),
            factories.ProductFactory(
                product_list=product_list,
                sku="123",
                name="def",
            ),
            factories.ProductFactory(
                product_list=product_list,
                sku="456",
                name="abcdef",
            ),
        ]

        for product in _products:
            db.session.add(product)
            db.session.flush()

            prices = factories.ProductPriceFactory.create_batch(2, product=product)

            db.session.add_all(prices)
            db.session.commit()

        return _products

    @pytest.fixture
    def response_data(self, product_list):
        data = {
            "id": product_list.id,
            "name": product_list.name,
            "products": [],
        }

        for product in product_list.products:
            product_row = {
                "id": product.id,
                "sku": product.sku,
                "name": product.name,
                "image": None,
                "prices": [],
            }

            for price in product.prices:
                product_row["prices"].append(
                    {
                        "value": float(price.value),
                        "currency_code": price.currency_code,
                    }
                )

            data["products"].append(product_row)

        return data

    def test_ok(self, as_user, user, product_list, products, response_data):
        response = as_user.get(self.url.format(product_list.id))

        assert response.status_code == 200
        assert response.json == response_data

    @pytest.mark.parametrize(
        "sort_by, expected_order",
        [
            ("sku", ["123", "456", "789"]),
            ("name", ["789", "456", "123"]),
        ],
    )
    def test_sort_by(self, as_user, product_list, products, sort_by, expected_order):
        response = as_user.get(self.url.format(product_list.id) + f"?sort_by={sort_by}")

        assert response.status_code == 200

        order = [p["sku"] for p in response.json["products"]]
        assert order == expected_order

    def test_filter_by_sku(self, as_user, product_list, products):
        response = as_user.get(self.url.format(product_list.id) + "?product_sku=123")

        assert response.status_code == 200

        products = response.json["products"]

        assert len(products) == 1
        assert products[0]["sku"] == "123"

    def test_filter_by_name(self, as_user, product_list, products):
        response = as_user.get(self.url.format(product_list.id) + "?product_name=abc")

        assert response.status_code == 200

        assert set(p["name"] for p in response.json["products"]) == {"abc", "abcdef"}

    def test_pagination(self, app, as_user, product_list, products):
        app.config["PAGINATION"] = 2

        response = as_user.get(self.url.format(product_list.id) + "?page=2")

        assert response.status_code == 200

        products = response.json["products"]

        assert len(products) == 1
        assert products[0]["sku"] == "456"

    def test_pagination_non_existent_page(self, app, as_user, product_list, products):
        response = as_user.get(self.url.format(product_list.id) + "?page=999")

        assert response.status_code == 404

    def test_unexisting(self, as_user):
        response = as_user.get(self.url.format(999))

        assert response.status_code == 404

    def test_other_user(self, product_list, as_other_user):
        response = as_other_user.get(self.url.format(product_list.id))

        assert response.status_code == 404

    def test_unauthorized(self, client, product_list):
        response = client.get(self.url.format(product_list.id))

        assert response.status_code == 401


class TestProductListReadAll:
    url = "/product_lists"

    def test_ok(self, as_user, product_list):
        response = as_user.get(self.url)

        assert response.status_code == 200
        assert response.json == {
            "results": [
                {
                    "id": product_list.id,
                    "name": product_list.name,
                }
            ]
        }

    def test_no_product_lists(self, as_user):
        response = as_user.get(self.url)

        assert response.status_code == 200
        assert response.json == {"results": []}

    def test_unauthorized(self, client):
        response = client.get(self.url)

        assert response.status_code == 401


class TestProductListDelete:
    url = "/product_lists/{}"

    def test_ok(self, as_user, product_list):
        response = as_user.delete(self.url.format(product_list.id))

        assert response.status_code == 204

    def test_unexisting(self, as_user):
        response = as_user.delete(self.url.format(999))

        assert response.status_code == 404

    def test_other_user(self, product_list, as_other_user):
        response = as_other_user.delete(self.url.format(product_list.id))

        assert response.status_code == 404

    def test_unauthorized(self, client, product_list):
        response = client.delete(self.url.format(product_list.id))

        assert response.status_code == 401
