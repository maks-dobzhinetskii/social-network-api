import json
import faker
import random
import requests


DEFAULT_NUMBER_OF_USERS = 3
DEFAULT_MAX_POSTS_PER_USER = 3
DEFAULT_MAX_LIKES_PER_USER = 3
DEFAULT_MAX_UNLIKES_PER_USER = 3

BASE_URL = 'http://127.0.0.1:8000/'


class AutomatedBot:
    def __init__(self, path_to_config_file):
        with open(path_to_config_file) as f:
            config = json.load(f)

        self.number_of_users = config.get('number_of_users', DEFAULT_NUMBER_OF_USERS)
        self.max_posts_per_user = config.get('max_posts_per_user', DEFAULT_MAX_POSTS_PER_USER)
        self.max_likes_per_user = config.get('max_likes_per_user', DEFAULT_MAX_LIKES_PER_USER)
        self.max_unlikes_per_user = config.get('max_unlikes_per_user', DEFAULT_MAX_UNLIKES_PER_USER)

        self.faker = faker.Faker()
        self.access_tokens = []
        self.posts_ids = []

    def perform_test(self):
        for i in range(self.number_of_users):
            self.sign_up_user()

        for access_token in self.access_tokens:
            for p in range(self.max_posts_per_user):
                self.create_post(access_token)

        for access_token in self.access_tokens:
            for n in range(self.max_likes_per_user):
                self.like_unlike_post(access_token, self.posts_ids, 'like')

        for access_token in self.access_tokens:
            for m in range(self.max_unlikes_per_user):
                self.like_unlike_post(access_token, self.posts_ids, 'unlike')

    def sign_up_user(self):
        username = self.faker.user_name()
        email = self.faker.email()
        password = self.faker.password()

        payload = {'username': username, 'email': email, 'password': password, 'password2': password}
        resp = requests.post(f'{BASE_URL}api/users/', json=payload)
        if resp.ok:
            print(resp.status_code)
            self.get_user_authentication_token(username, password)
        else:
            print(f'{resp.status_code} - {resp.text}')

    def get_user_authentication_token(self, username, password):
        payload = {'username': username, 'password': password}
        resp = requests.post(f'{BASE_URL}token/', json=payload)
        if resp.ok:
            print(resp.status_code)
            self.access_tokens.append(resp.json()['access'])
        else:
            print(f'{resp.status_code} - {resp.text}')

    def create_post(self, access_token):
        title = self.faker.sentence()
        content = self.faker.sentence()

        headers = {'Authorization': 'Bearer ' + access_token}
        payload = {'title': title, 'content': content}

        resp = requests.post(f'{BASE_URL}api/posts/', json=payload, headers=headers)
        if resp.ok:
            print(resp.status_code)
            self.posts_ids.append(resp.json()['id'])
        else:
            print(f'{resp.status_code} - {resp.text}')

    def like_unlike_post(self, access_token, posts_ids, action):
        post_id = random.choice(posts_ids)
        headers = {'Authorization': 'Bearer ' + access_token}

        resp = requests.post(f'{BASE_URL}api/posts/{post_id}/{action}/', headers=headers)

        if resp.ok:
            print(resp.status_code)
        else:
            print(f'{resp.status_code} - {resp.text}')


if __name__ == '__main__':
    bot = AutomatedBot('scripts/config.json')
    bot.perform_test()
