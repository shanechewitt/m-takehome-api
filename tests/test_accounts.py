from unittest.mock import patch
from app.services.account_service import AccountService
from app.models.account import AccountCreate
from .mocks.response_mocks import *

# Success Cases
def test_create_account_success(client, mock_supabase_account_success):
    # Arrange
    valid_params = {"customer_id": 1, "name": "Test Account", "initial_amount": 100.00}
    account_create = AccountCreate(**valid_params)
    with patch('app.services.account_service.AccountService._create_account_model') as mock_create_acc_model:
        acc_model_create_to_return = {
            "customer_id": 1,
            "balance": 100.00,
            "name": "Test Account",
            "account_number": "111111111111",
            "routing_number": "999999999"
        }
        mock_create_acc_model.return_value = acc_model_create_to_return

        # Act
        response = client.post("/api/accounts/create", json=valid_params)

        # Assert
        response_data = response.json()
        assert response.status_code == 200
        assert response_data == MOCK_ACCOUNT

        mock_create_acc_model.assert_called_once_with(account_create)
        mock_supabase_account_success.table.assert_called_once_with("BankAccounts")
        mock_supabase_account_success.table().insert.assert_called_once_with(acc_model_create_to_return)

# Edge Cases - Validation
def test_create_account_error_empty_name(client):
    # Arrange
    empty_name_params = {
        "customer_id": 1,
        "name": "",
        "initial_amount": 100.00
    }
    # Act
    response = client.post("/api/accounts/create", json=empty_name_params)
    # Assert
    response_error = response.json()
    assert response.status_code == 400
    assert response.is_error == True
    assert response_error["detail"] == "Bank account name cannot be empty"

def test_create_account_error_negative_amount(client):
    # Arrange
    negative_amount_params = {
        "customer_id": 1,
        "name": "Test Account",
        "initial_amount": -100.00
    }
    # Act
    response = client.post("/api/accounts/create", json=negative_amount_params)
    # Assert
    response_error = response.json()
    assert response.status_code == 400
    assert response.is_error == True
    assert response_error["detail"] == "Bank account balance cannot be negative"

# Database Errors
def test_create_customer_error_database(client, mock_supabase_account_error):
    # Arrange
    valid_params = {"customer_id": 1, "name": "Test Account", "initial_amount": 100.00}
    with patch('app.services.account_service.AccountService._create_account_model') as mock_create_acc_model:
        acc_model_create_to_return = {
            "customer_id": 1,
            "balance": 100.00,
            "name": "Test Account",
            "account_number": "111111111111",
            "routing_number": "999999999"
        }
        mock_create_acc_model.return_value = acc_model_create_to_return
        # Act
        response = client.post("/api/accounts/create", json=valid_params)
        # Assert
        response_error = response.json()
        assert response.status_code == 500
        assert response.is_error == True
        assert response_error["detail"] == "Bank account creation failed: Database error"

        mock_supabase_account_error.table.assert_called_once_with("BankAccounts")
        mock_supabase_account_error.table().insert.assert_called_once_with(acc_model_create_to_return)

# Helper Tests
# Generate Account Numbers
def test_generate_account_numbers(client):
    # Arrange

    # Act
    acc_num, routing_num = AccountService._generate_account_numbers()
    # Assert
    assert len(acc_num) == 12
    assert len(routing_num) == 9

# Generate Account Model
def test_generate_account_model(client):
    # Arrange
    account_create_params = {"customer_id": 1, "name": "Test Account", "initial_amount": 100.00}
    account_create_obj = AccountCreate(**account_create_params)
    with patch('app.services.account_service.AccountService._generate_account_numbers') as mock_generate_numbers:
        mock_generate_numbers.return_value = ("111111111111", "999999999")
        # Act
        account_model = AccountService._create_account_model(account_create_obj)
        # Assert
        assert account_model["customer_id"] == account_create_obj.customer_id
        assert account_model["name"] == account_create_obj.name
        assert account_model["balance"] == account_create_obj.initial_amount
        assert account_model["account_number"] == "111111111111"
        assert account_model["routing_number"] == "999999999"

