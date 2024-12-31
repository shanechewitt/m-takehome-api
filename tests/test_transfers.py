from unittest.mock import call, patch
from .mocks.response_mocks import MOCK_TRANSFER_HISTORY

# Create Transfer
## Success Cases

def test_create_transfer_success(client, mock_supabase_create_transfer_success):
    # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
        with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
            valid_transfer_params = {
                "sending_account_number": "111111111111",
                "sending_routing_number": "999999999",
                "receiving_account_number": "222222222222",
                "receiving_routing_number": "777777777",
                "transfer_amount": 10.00
            }
            expected_insert = valid_transfer_params
            expected_insert["status"] = "Success"
            # Act
            response = client.post("/api/transfers/create", json=valid_transfer_params)
            # Assert
            assert response.status_code == 200
            mock_get_balance.assert_has_calls([call(valid_transfer_params["sending_account_number"], valid_transfer_params["sending_routing_number"]),
                                               call(valid_transfer_params["receiving_account_number"], valid_transfer_params["receiving_routing_number"])])
            mock_update_balance.assert_has_calls([call(valid_transfer_params["sending_account_number"], valid_transfer_params["sending_routing_number"], -valid_transfer_params["transfer_amount"]),
                                                   call(valid_transfer_params["receiving_account_number"], valid_transfer_params["receiving_routing_number"], valid_transfer_params["transfer_amount"])])
            
            mock_supabase_create_transfer_success.table.assert_called_once_with("Transfers")
            mock_supabase_create_transfer_success.table().insert.assert_called_once_with(expected_insert)

## Edge Cases
def test_create_transfer_sender_account_not_exist(client):
    # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
        mock_get_balance.side_effect = [
            None,
            100.00
        ]
        with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
            valid_transfer_params = {
                "sending_account_number": "111111111111",
                "sending_routing_number": "999999999",
                "receiving_account_number": "222222222222",
                "receiving_routing_number": "777777777",
                "transfer_amount": 10.00
            }
            # Act
            response = client.post("/api/transfers/create", json=valid_transfer_params)
            # Assert
            assert response.status_code == 404
            assert response.json()["detail"] == "Sender account does not exist"

def test_create_transfer_receiver_account_not_exist(client):
     # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
        mock_get_balance.side_effect = [
            100.00,
            None
        ]
        with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
            valid_transfer_params = {
                "sending_account_number": "111111111111",
                "sending_routing_number": "999999999",
                "receiving_account_number": "222222222222",
                "receiving_routing_number": "777777777",
                "transfer_amount": 10.00
            }
            # Act
            response = client.post("/api/transfers/create", json=valid_transfer_params)
            # Assert
            assert response.status_code == 404
            assert response.json()["detail"] == "Receiving account does not exist"

def test_create_transfer_receiver_sender_insufficient_funds(client, mock_supabase_create_transfer_success):
    # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
        with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
            too_large_transfer_params = {
                "sending_account_number": "111111111111",
                "sending_routing_number": "999999999",
                "receiving_account_number": "222222222222",
                "receiving_routing_number": "777777777",
                "transfer_amount": 105.00 # Greater than balance of 100
            }
            expected_insert = too_large_transfer_params
            expected_insert["status"] = "Failed: Insufficient Funds"
            # Act
            response = client.post("/api/transfers/create", json=too_large_transfer_params)
            # Assert
            assert response.status_code == 400
            assert response.json()["detail"] == "Sending account has insufficient funds"

def test_create_transfer_amount_negative(client, mock_supabase_create_transfer_success):
    # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
            with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
                negative_transfer_params = {
                    "sending_account_number": "111111111111",
                    "sending_routing_number": "999999999",
                    "receiving_account_number": "222222222222",
                    "receiving_routing_number": "777777777",
                    "transfer_amount": -105.00 # Negative transfer
                }
                # Act
                response = client.post("/api/transfers/create", json=negative_transfer_params)
                # Assert
                assert response.status_code == 400
                assert response.json()["detail"] == "Transfer amount must be non-zero and positive"

## Database Error
def test_create_transfer_database_error(client, mock_supabase_create_transfer_database_error):
    # Arrange
    with patch('app.services.account_service.AccountService.get_account_balance_internal', return_value=100.00) as mock_get_balance:
        with patch('app.services.account_service.AccountService.update_account_balance') as mock_update_balance:
            valid_transfer_params = {
                "sending_account_number": "111111111111",
                "sending_routing_number": "999999999",
                "receiving_account_number": "222222222222",
                "receiving_routing_number": "777777777",
                "transfer_amount": 10.00
            }
            # Act
            response = client.post("/api/transfers/create", json=valid_transfer_params)
            # Assert
            assert response.status_code == 500
            assert response.json()["detail"] == "Transfer failed: Database error"


# Get Transfer History
## Success
def test_get_transfer_history_success(client, mock_supabase_get_transfer_list_success):
    # Arrange
    account_number = "111111111111"
    # Act
    response = client.get(f"/api/transfers/transfer-history/{account_number}")

    # Assert
    assert response.status_code == 200
    assert response.json() == MOCK_TRANSFER_HISTORY

    table = mock_supabase_get_transfer_list_success.table
    table.assert_called_once_with("Transfers")
    table.return_value.select.assert_called_once_with("sending_account_number, receiving_account_number, transfer_amount, status")
    table.return_value.select.return_value.or_.assert_called_once_with(f"sending_account_number.eq.{account_number},receiving_account_number.eq.{account_number}")

## Database Error
def test_get_transfer_history_database_error(client, mock_supabase_get_transfer_list_database_error):
    # Arrange
    account_number = "111111111111"
    # Act
    response = client.get(f"/api/transfers/transfer-history/{account_number}")
    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == "Transfer fistory failed: Database error"

    table = mock_supabase_get_transfer_list_database_error.table
    table.assert_called_once_with("Transfers")
    table.return_value.select.assert_called_once_with("sending_account_number, receiving_account_number, transfer_amount, status")
    table.return_value.select.return_value.or_.assert_called_once_with(f"sending_account_number.eq.{account_number},receiving_account_number.eq.{account_number}")
