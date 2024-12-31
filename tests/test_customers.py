# Success Cases
from .mocks.response_mocks import MOCK_CUSTOMER_LIST

def test_create_customer_success(client, mock_supabase_customer_success):
    # Arrange
    valid_params = {"name": "Test Customer"}
    # Act    
    response = client.post("/api/customers/create", json=valid_params)

    # Assert
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == 1
    assert response_data["name"] == "Test Customer"

    mock_supabase_customer_success.table.assert_called_once_with("Customers")
    mock_supabase_customer_success.table().insert.assert_called_once_with({"name": "Test Customer"})

# Edge Cases - Validation

def test_create_customer_error_empty_name(client):
    # Arrange
    empty_name_params = {"name": ""}
    # Act
    response = client.post("/api/customers/create", json=empty_name_params)
    # Assert
    response_error = response.json()
    assert response.status_code == 400
    assert response.is_error == True
    assert response_error["detail"] == "Customer name cannot be empty"

def test_create_customer_error_no_name(client):
    # Arrange
    no_params = {}
    # Act
    response = client.post("/api/customers/create", json=no_params)
    # Assert
    assert response.status_code == 422 # PyDantic Type Error
    assert response.is_error == True

# Database Errors
def test_create_customer_error_database(client, mock_supabase_customer_error):
    # Arrange
    valid_params={ "name": "Test Customer" }
    # Act
    response = client.post("/api/customers/create", json=valid_params)
    # Assert
    response_error = response.json()
    assert response.status_code == 500
    assert response.is_error == True
    assert response_error["detail"] == "Customer creation failed: Database error"
    
    mock_supabase_customer_error.table.assert_called_once_with("Customers")
    mock_supabase_customer_error.table().insert.assert_called_once_with(valid_params)

# Customer List Get
def test_customer_list_get_success(client, mock_supabase_customer_list_success):
    # Arrange
    # Act
    response = client.get("/api/customers/customer-list")
    # Assert
    assert response.status_code == 200
    assert response.json() == MOCK_CUSTOMER_LIST

    mock_supabase_customer_list_success.table.assert_called_once_with("Customers")
    mock_supabase_customer_list_success.table.return_value.select.assert_called_once_with("id, name")

def test_customer_list_get_database_error(client, mock_supabase_customer_list_error):
    # Arrange
    # Act
    response = client.get("/api/customers/customer-list")
    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == "Customer List GET failed: Database error"

