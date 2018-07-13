import json
import unittest
from project import db
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


USERS = [
    ['jeff', 'jeff@lindholm.org', b'jeff'],
    ['iryna', 'iryna@lindholm.org', b'iryna']
]


class TestUserService(BaseTestCase):
    """Tests for the users Service."""

    def test_users(self):
        """Ensure the /ping route does the right thing"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': USERS[0][0],
                    'email': USERS[0][1]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(f'{USERS[0][1]} was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
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
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'michael@mherman.org'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': USERS[0][0],
                    'email': USERS[0][1]
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': USERS[0][0],
                    'email': USERS[0][1]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user(USERS[0][0], USERS[0][1])
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(USERS[0][0], data['data']['username'])
            self.assertIn(USERS[0][1], data['data']['email'])
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

    def test_all_users(self):
        for u in USERS:
            add_user(u[0], u[1])
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), len(USERS))
            for idx, u in enumerate(USERS):
                self.assertIn(u[0], data['data']['users'][idx]['username'])
                self.assertIn(u[1], data['data']['users'][idx]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        for u in USERS:
            add_user(u[0], u[1])
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            for _, u in enumerate(USERS):
                self.assertIn(u[2], response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        user = USERS[0]
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username=user[0], email=user[1]),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(user[2], response.data)


if __name__ == '__main__':
    unittest.main()
