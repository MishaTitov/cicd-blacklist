import sys
import os
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import the main Flask app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.client = app.test_client()

### HEALTH ###
    def test_health_route_success(self):
        logger.info(f"TEST /health")
        # Test the /health route under normal conditions
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "OK")

### GET_LIST ###
    @patch('routes.GET_list.load_data')  # Mock the load_data function
    def test_get_list_route_success(self, mock_load_data):
        logger.info(f"TEST /GET_list")
        # Mock the load_data function to return a sample blacklist
        mock_load_data.return_value = [{"name": "Alice"}, {"name": "Bob"}]

        # Make a GET request to /api/get_list
        response = self.client.get('/api/get_list')

        # Assert the response status code and JSON data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"name": "Alice"}, {"name": "Bob"}])

### POST_PERSON ###  
    @patch('routes.POST_person.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_post_person_success(self, mock_connect_to_mongodb):
        logger.info(f"TEST /POST_list 1 of 2")
        # Mock the MongoDB collection and its insert_one method
        mock_collection = MagicMock()
        mock_connect_to_mongodb.return_value = mock_collection

        # Make a POST request with valid form data
        response = self.client.post('/api/add', data={'name': 'Alice', 'reason': 'Testing'})

        # Assert the response status code and JSON data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Person added successfully"})

        # Verify that insert_one was called with the correct data
        mock_collection.insert_one.assert_called_once_with({'name': 'Alice', 'reason': 'Testing'})

    @patch('routes.POST_person.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_post_person_missing_fields(self, mock_connect_to_mongodb):
        logger.info(f"TEST /POST_list 2 of 2")
        # Make a POST request with missing form data
        response = self.client.post('/api/add', data={'name': 'Alice'})  # Missing 'reason'

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Name and reason are required"})

        # Verify that connect_to_mongodb was not called
        mock_connect_to_mongodb.assert_not_called()

### GET_BY_NAME ###
    @patch('routes.GET_by_name.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_get_by_name_success(self, mock_connect_to_mongodb):
        logger.info(f"TEST /GET_by_name 1 of 2")
        # Mock the MongoDB collection and its find method
        mock_collection = MagicMock()
        mock_connect_to_mongodb.return_value = mock_collection

        # Mock the find method to return a filtered list
        mock_collection.find.return_value = [{"name": "Alice"}, {"name": "Bob"}]

        # Make a GET request with a name query
        response = self.client.get('/api/search?name=alice')

        # Assert the response status code and JSON data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"name": "Alice"}, {"name": "Bob"}])

        # Verify that find was called with the correct query
        mock_collection.find.assert_called_once_with({"name": {"$regex": "alice", "$options": "i"}}, {'_id': 0})

    @patch('routes.GET_by_name.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_get_by_name_no_name(self, mock_connect_to_mongodb):
        logger.info(f"TEST /GET_by_name 2 of 2")
        # Make a GET request without a name query
        response = self.client.get('/api/search')

        # Assert the response status code and JSON data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

        # Verify that connect_to_mongodb was not called
        mock_connect_to_mongodb.assert_not_called()

### DELETE_PERSON ###
    @patch('routes.DELETE_person.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_delete_person_success(self, mock_connect_to_mongodb):
        logger.info(f"TEST /DELETE_person 1 of 3")
        # Mock the MongoDB collection and its delete_one method
        mock_collection = MagicMock()
        mock_connect_to_mongodb.return_value = mock_collection

        # Mock the delete_one method to return a result with deleted_count = 1
        mock_collection.delete_one.return_value.deleted_count = 1

        # Make a DELETE request with a valid name
        response = self.client.delete('/api/delete', data={'name': 'Alice'})

        # Assert the response status code and JSON data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Person deleted successfully"})

        # Verify that delete_one was called with the correct query
        mock_collection.delete_one.assert_called_once_with({"name": "Alice"})

    @patch('routes.DELETE_person.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_delete_person_missing_name(self, mock_connect_to_mongodb):
        logger.info(f"TEST /DELETE_person 2 of 3")
        # Make a DELETE request without a name
        response = self.client.delete('/api/delete')

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Name is required"})

        # Verify that connect_to_mongodb was not called
        mock_connect_to_mongodb.assert_not_called()

    @patch('routes.DELETE_person.connect_to_mongodb')  # Mock the connect_to_mongodb function
    def test_delete_person_not_found(self, mock_connect_to_mongodb):
        logger.info(f"TEST /DELETE_person 3 of 3")
        # Mock the MongoDB collection and its delete_one method
        mock_collection = MagicMock()
        mock_connect_to_mongodb.return_value = mock_collection

        # Mock the delete_one method to return a result with deleted_count = 0
        mock_collection.delete_one.return_value.deleted_count = 0

        # Make a DELETE request with a name that doesn't exist
        response = self.client.delete('/api/delete', data={'name': 'Unknown'})

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Person not found"})

if __name__ == "__main__":
    unittest.main()