import random
import time
import unittest
from pprint import pprint

from radish_rest.sdk.rest import HTTPException

from conduit.client import ConduitClient, ConduitConfig


class TestBackend(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.conduit = ConduitClient(ConduitConfig())
        self.conduit_assert = ConduitClient(ConduitConfig())
        self.random_string = self._get_random_string()

    @staticmethod
    def _get_random_string():
        return f"{int(time.time()) + random.choice(range(1000))}"

    def _get_user_email_password(self):
        return self.random_string, f"{self.random_string}@tw.pl", self.random_string

    def test_register_user(self):
        user, email, password = self._get_user_email_password()
        self.conduit.users.register_user(user, email, password)

        response = self.conduit_assert.users.login_user(email, password)
        assert response.status_code == 200

    def test_register_the_same_user(self):
        user, email, password = self._get_user_email_password()
        self.conduit.users.register_user(user, email, password)

        try:
            self.conduit_assert.users.register_user(user, email, password)
        except HTTPException as e:
            assert e.status == 422
            assert e.response.json()["errors"]["body"][0] == "User already registered"
        else:
            raise AssertionError("Exception not raised")

    def test_user_info(self):
        user, email, password = self._get_user_email_password()
        self.conduit.users.register_user(user, email, password)

        self.conduit_assert.users.login_user(email, password)
        response = self.conduit_assert.users.get_current_user()
        assert response.status_code == 200
        assert response.json()["user"]["email"] == email
        assert response.json()["user"]["username"] == user

    def test_article_available_for_not_logged_user(self):
        user, email, password = self._get_user_email_password()
        self.conduit.users.register_user(user, email, password)
        response = self.conduit.articles.create_article(f"TEST - {user}",
                                                        "test description",
                                                        "test body",
                                                        [f"mario{user}"])

        article_response = self.conduit_assert.articles.get_article(response.json()["article"]["slug"])
        pprint(article_response.json())
