from copy import deepcopy
from typing import List

from radish_rest.sdk.rest import RestConfig, RestClient
from requests import Response


class ConduitConfig(RestConfig):
    def __init__(self):
        super().__init__()
        self.url = "http://localhost:5000/api"
        self.connect_timeout = 15
        self.read_timeout = 10
        self.number_of_retries = 0

    def set_properties(self, url):
        self.url = url
        return self


class ConduitGroupApi(object):
    def __init__(self, conduit_client: RestClient) -> None:
        super().__init__()
        self.client = conduit_client


class Users(ConduitGroupApi):
    def login_user(self, email, password) -> Response:
        response = self.client.post("/users/login", json={
            "user": {
                "email": email,
                "password": password
            }
        })
        self.client.check_status(response)
        self.client.default_kwargs["headers"] = {"Authorization": f"Token {response.json()['user']['token']}"}
        return response

    def register_user(self, username, email, password) -> Response:
        response = self.client.post("/users", json={
            "user": {
                "username": username,
                "email": email,
                "password": password
            }
        })
        self.client.check_status(response)
        self.client.default_kwargs["headers"] = {"Authorization": f"Token {response.json()['user']['token']}"}
        return response

    def get_current_user(self) -> Response:
        response = self.client.get("/user")
        self.client.check_status(response)
        return response

    def update_current_user(self, email=None, username=None, bio=None, image=None, password=None) -> Response:
        user = {
            "user": {
                "email": email,
                "username": username,
                "bio": bio,
                "image": image,
                "password": password
            }
        }
        copy_user = deepcopy(user)
        for k, v in copy_user["user"].items():
            if v is None:
                del user["user"][k]
        response = self.client.put("/user", json=user)
        self.client.check_status(response)
        return response


class Profiles(ConduitGroupApi):
    def get_profile(self):
        pass

    def follow_user(self):
        pass

    def unfollow_user(self):
        pass


class Articles(ConduitGroupApi):
    def get_recent_articles_from_users_you_follow(self, limit: int = 20, offset: int = 0) -> Response:
        params = {"limit": limit, "offset": offset}
        response = self.client.get("/articles/feed", params=params)
        self.client.check_status(response)
        return response

    def get_recent_articles_globally(self,
                                     tag: str = None,
                                     author: str = None,
                                     favorited: str = None,
                                     limit: int = 20,
                                     offset: int = 0):
        params = {"limit": limit, "offset": offset}
        if tag is not None:
            params.update({"tag": tag})
        if author is not None:
            params.update({"author": author})
        if favorited is not None:
            params.update({"favorited": favorited})
        response = self.client.get("/articles", params=params)
        self.client.check_status(response)
        return response

    def create_article(self, title, description, body, tags: List[str]) -> Response:
        """
        example body:
        An h1 header
        ============

        Paragraphs are separated by a blank line.

        2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
        look like:

          * this one
          * that one
          * the other one

        Note that --- not considering the asterisk --- the actual text
        content starts at 4-columns in.

        > Block quotes are
        > written like so.favorited
        >
        > They can span multiple paragraphs,
        > if you like.
        """
        response = self.client.post("/articles", json={
            "article": {
                "title": title,
                "description": description,
                "body": body,
                "tagList": tags
            }
        })
        self.client.check_status(response)
        return response

    def get_article(self, slug) -> Response:
        response = self.client.get(f"/articles/{slug}")
        self.client.check_status(response)
        return response

    def update_article(self, slug, title, description, body):
        response = self.client.put(f"/articles/{slug}", json={
            "article": {
                "title": title,
                "description": description,
                "body": body,
            }
        })
        self.client.check_status(response)
        return response

    def delete_article(self, slug) -> Response:
        response = self.client.delete(f"/articles/{slug}")
        self.client.check_status(response)
        return response


class Comments(ConduitGroupApi):
    def get_comments_for_article(self):
        pass

    def create_comment_for_article(self):
        pass

    def delete_comment_for_article(self):
        pass


class Favorites(ConduitGroupApi):
    def favorite_article(self):
        pass

    def unfavorite_article(self):
        pass


class Tags(ConduitGroupApi):
    def get_tags(self):
        pass


class ConduitClient(RestClient):
    def __init__(self, rest_config):
        super().__init__(rest_config)
        self.users = Users(self)
        self.profiles = Profiles(self)
        self.articles = Articles(self)
        self.comments = Comments(self)
        self.favorites = Favorites(self)
        self.tags = Tags(self)
