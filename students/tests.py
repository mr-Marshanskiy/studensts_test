from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from students.models.students import Student
from users.models.users import Group

User = get_user_model()


class StudentAPITestCase(TestCase):
    def get_token(self):
        joser_url = '/api/auth/jwt/create/'
        response = self.client.post(
            joser_url,
            data={
                'username': self.user.username,
                'password': 'testpassword'}
        )
        token_data = response.json()
        token = token_data['access']
        return token

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        group, created = Group.objects.get_or_create(
            code='director',
            defaults={
                'name': 'director',
            }
        )
        self.user.groups.add(group)
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)

    def test_get_retrieve(self):
        student_id = self._create_student().pk
        response = self.client.get(f'/api/students/{student_id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        response = self.client.post(f'/api/students/', data=self._get_student_data())
        self.assertEqual(response.status_code, 201)

    def _create_student(self):
        return Student.objects.create(
            **self._get_student_data()
        )

    def _get_student_data(self):
        return {
                'first_name': 'First',
                'last_name': 'Last',
                'middle_name': 'Test',
            }
