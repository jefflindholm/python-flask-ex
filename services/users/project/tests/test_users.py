import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase

email = 'email@email.com'


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):

    """Tests for the Users Service."""
    def test_main_add_user(self):
        """Ensure you can add a new user and that it is in the database"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='user3', email='user3@bar.com'),
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertIn(b'user3', response.data)

    def test_main_with_users(self):
        """Ensure the main route does the right thing with users present"""
        add_user('user1', 'user1@foo.com')
        add_user('user2', 'user2@foo.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users</p>', response.data)
            self.assertIn(b'user1', response.data)
            self.assertIn(b'user2', response.data)

    def test_main_no_users(self):
        """Ensure the main route does the right thing with no users"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users</p>', response.data)

    def test_all_users(self):
        """Ensure all users are returned"""
        add_user(username="jeff", email=email)
        add_user(username="iryna", email=f'iryna.{email}')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            users = data['data']['users']
            for user in users:
                if user['username'] == 'iryna':
                    self.assertIn(f'iryna.{email}', user['email'])
                else:
                    self.assertIn('jeff', user['username'])
                    self.assertIn(email, user['email'])
            self.assertIn('success', data['status'])

    def test_single_user(self):
        """Ensure get single user works as expected"""
        user = add_user(username="jeff", email=email)
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('jeff', data['data']['username'])
            self.assertIn(email, data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('ping', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'jeff',
                'email': email
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(f'{email} was added!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a username."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': email}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_dulicate_json_keys(self):
        """Ensure error is thrown if the JSON object has duplicate email"""
        with self.client:
            email = 'dup@dup.com'
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'unused',
                    'email': email
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'unused',
                    'email': email
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()
