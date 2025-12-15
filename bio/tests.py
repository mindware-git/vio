import json
from unittest.mock import patch, call
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages


class FileUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse("upload_file")

    def test_upload_page_get_request(self):
        """Test that the upload page loads correctly with a GET request."""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload.html")

    @patch("bio.views.call_command")
    def test_upload_valid_json_file(self, mock_call_command):
        """Test uploading a valid JSON file."""
        json_data = {"name": "Test Person", "biography": "A test biography."}
        json_content = json.dumps(json_data).encode("utf-8")
        file = SimpleUploadedFile(
            "test.json", json_content, content_type="application/json"
        )

        response = self.client.post(self.upload_url, {"file": file}, follow=True)

        self.assertRedirects(response, self.upload_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "File processed successfully!")
        self.assertEqual(mock_call_command.call_count, 1)
        # Get the call arguments
        args, kwargs = mock_call_command.call_args
        # Check the command name
        self.assertEqual(args[0], "load_result_data")
        # Check the file path argument
        self.assertTrue(args[1].startswith("--file="))
        self.assertTrue(args[1].endswith(".json"))
        # Check the update flag
        self.assertEqual(args[2], "--update")

    def test_upload_invalid_file_type(self):
        """Test uploading a file that is not a .json file."""
        file = SimpleUploadedFile(
            "test.txt", b"some content", content_type="text/plain"
        )
        response = self.client.post(self.upload_url, {"file": file}, follow=True)

        self.assertRedirects(response, self.upload_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Invalid file type. Please upload a .json file."
        )

    def test_upload_no_file(self):
        """Test submitting the form with no file selected."""
        response = self.client.post(self.upload_url, {}, follow=True)
        self.assertRedirects(response, self.upload_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "No file part")
