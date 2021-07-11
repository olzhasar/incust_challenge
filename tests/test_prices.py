from api.models import ProductPrice


class TestPriceCreate:
    url = "/products/{}/prices"

    def test_ok(self, as_user, product):
        response = as_user.post(
            self.url.format(product.id),
            json=[
                {"currency_code": "USD", "value": 100},
                {"currency_code": "GBP", "value": 80},
            ],
        )

        assert response.status_code == 201
        assert response.json == [
            {"currency_code": "USD", "value": 100},
            {"currency_code": "GBP", "value": 80},
        ]

        prices = ProductPrice.query.filter_by(product_id=product.id).order_by("value")

        assert prices[0].currency_code == "GBP"
        assert prices[0].value == 80
        assert prices[1].currency_code == "USD"
        assert prices[1].value == 100

    def test_duplicated_currency_code(self, as_user, product, price):
        response = as_user.post(
            self.url.format(product.id),
            json=[
                {"currency_code": price.currency_code, "value": 100},
            ],
        )

        assert response.status_code == 400

    def test_unauthorized(self, client, product):
        response = client.post(
            self.url.format(product.id),
            json=[
                {"currency_code": "USD", "value": 100},
                {"currency_code": "GBP", "value": 80},
            ],
        )

        assert response.status_code == 401

    def test_other_users_product(self, as_other_user, product):
        response = as_other_user.post(
            self.url.format(product.id),
            json=[
                {"currency_code": "USD", "value": 100},
                {"currency_code": "GBP", "value": 80},
            ],
        )

        assert response.status_code == 400
        assert response.json["detail"] == "Invalid product_id"


class TestPriceDelete:
    url = "/products/{}/prices/{}"

    def test_ok(self, as_user, product, price):
        response = as_user.delete(self.url.format(product.id, price.currency_code))

        assert response.status_code == 204

    def test_unexisting(self, as_user):
        response = as_user.delete(self.url.format(999, "USD"))

        assert response.status_code == 404

    def test_other_user(self, as_other_user, product, price):
        response = as_other_user.delete(
            self.url.format(product.id, price.currency_code)
        )

        assert response.status_code == 404

    def test_unauthorized(self, client, product, price):
        response = client.delete(self.url.format(product.id, price.currency_code))

        assert response.status_code == 401
