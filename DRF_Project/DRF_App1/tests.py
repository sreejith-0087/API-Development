from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User

class CSVUploadTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_csv_upload(self):
        csv_data = "name,email,age\nJohn Doe,john@example.com,30"
        csv_file = SimpleUploadedFile("test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 1)
        self.assertEqual(response.json()['total_rejected'], 0)

    def test_invalid_csv_upload(self):
        csv_data = "name,email,age\nInvalid Email,invalid-email,25"
        csv_file = SimpleUploadedFile("test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 0)
        self.assertEqual(response.json()['total_rejected'], 1)

    def test_invalid_file_format(self):
        invalid_file = SimpleUploadedFile("test.txt", b"Invalid file content", content_type="text/plain")
        response = self.client.post('/upload/', {'file': invalid_file})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_missing_required_fields(self):
        csv_data = "name,email\nJohn Doe,john@example.com"
        csv_file = SimpleUploadedFile("test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 0)
        self.assertEqual(response.json()['total_rejected'], 1)
        self.assertIn('Missing required fields', response.json()['errors'][0]['error'])

    def test_invalid_age(self):
        csv_data = "name,email,age\nJohn Doe,john@example.com,150"
        csv_file = SimpleUploadedFile("test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 0)
        self.assertEqual(response.json()['total_rejected'], 1)
        self.assertIn('Age must be between 0 and 120', response.json()['errors'][0]['error']['age'][0])

    def test_duplicate_email(self):
        User.objects.create(name="Existing User", email="john@example.com", age=30)
        csv_data = "name,email,age\nJohn Doe,john@example.com,30"
        csv_file = SimpleUploadedFile("test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 0)
        self.assertEqual(response.json()['total_rejected'], 1)

        errors = response.json()['errors']
        self.assertTrue(
            any('user with this email already exists.' in str(error['error'].get('email', [])) for error in errors))

    def test_large_csv_file(self):
        csv_data = "name,email,age\n"
        for i in range(1000):
            csv_data += f"User {i},user{i}@example.com,{i % 120}\n"

        csv_file = SimpleUploadedFile("large_test.csv", csv_data.encode(), content_type="text/csv")
        response = self.client.post('/upload/', {'file': csv_file})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['total_saved'], 1000)
        self.assertEqual(response.json()['total_rejected'], 0)