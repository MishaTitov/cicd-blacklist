import requests
import os
import sys

# Base URL of your API
BASE_URL = os.getenv("BASE_URL", "http://localhost")  # Replace with your API's URL

# Helper function to print test results and raise an error if the test fails
def assert_test(test_name, condition, error_message):
    if condition:
        print(f"{test_name}: PASS")
    else:
        print(f"{test_name}: FAIL - {error_message}")
        raise AssertionError(f"{test_name} failed: {error_message}")

# Step 1: Homepage
def test_homepage():
    response = requests.get(f"{BASE_URL}/")
    assert_test("Homepage", response.status_code == 200, f"Expected status code 200, got {response.status_code}")

# Step 2: Get All List
def test_get_all_list():
    response = requests.get(f"{BASE_URL}/api/get_list")
    assert_test("Get All List", response.status_code == 200 and isinstance(response.json(), list), 
                f"Expected status code 200 and a list, got {response.status_code} and {type(response.json())}")

# Step 3: Add New Person
def test_add_new_person():
    new_person = {"name": "Tester Testerov", "reason": "Too much tests"}
    response = requests.post(f"{BASE_URL}/api/add", data=new_person)
    assert_test("Add New Person", response.status_code == 201, 
                f"Expected status code 201, got {response.status_code}")
    return new_person["name"]  # Return the name of the added person

# Step 4: Get List After Adding
def test_get_list_after_add(person_name):
    response = requests.get(f"{BASE_URL}/api/get_list")
    persons = response.json()
    person_exists = any(person["name"] == person_name for person in persons)
    assert_test("Get List After Adding", person_exists, 
                f"Person '{person_name}' not found in the list")

# Step 5: Search Added Person
def test_search_added_person(person_name):
    response = requests.get(f"{BASE_URL}/api/search?name={person_name}")
    assert_test("Search Added Person", response.status_code == 200 and response.json()[0]["name"] == person_name, 
                f"Expected status code 200 and person '{person_name}', got {response.status_code} and {response.json()}")

# Step 6: Delete Added Person
def test_delete_added_person(person_name):
    person_to_delete = {"name": person_name}
    response = requests.delete(f"{BASE_URL}/api/delete", data=person_to_delete)
    assert_test("Delete Added Person", response.json().get("message") == "Person deleted successfully", 
                f"Expected 'Person deleted successfully', got {response.json()}")

# Step 7: Get List After Deletion
def test_get_list_after_delete(person_name):
    response = requests.get(f"{BASE_URL}/api/get_list")
    persons = response.json()
    person_exists = any(person["name"] == person_name for person in persons)
    assert_test("Get List After Deletion", not person_exists, 
                f"Person '{person_name}' still exists in the list")

# Step 8: Search Deleted Person
def test_search_deleted_person(person_name):
    response = requests.get(f"{BASE_URL}/api/search?name={person_name}")
    assert_test("Search Deleted Person", not bool(response.json()), 
                f"Expected empty response, got {response.json()}")

# Main function to run all tests
def run_tests():
    try:
        test_homepage()
        test_get_all_list()
        person_name = test_add_new_person()
        test_get_list_after_add(person_name)
        test_search_added_person(person_name)
        test_delete_added_person(person_name)
        test_get_list_after_delete(person_name)
        test_search_deleted_person(person_name)
        print("All tests passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)  # Exit with a non-zero status code to indicate failure

if __name__ == "__main__":
    run_tests()