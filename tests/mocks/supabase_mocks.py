import pytest
from unittest.mock import patch
from .response_mocks import *

# CREATE Customer
@pytest.fixture
def mock_supabase_customer_success():
    with patch('app.services.customer_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.return_value.data = [MOCK_CUSTOMER]
        yield mock

@pytest.fixture
def mock_supabase_customer_error():
    with patch('app.services.customer_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.side_effect = Exception("Database error")
        yield mock
        
# CREATE Account
@pytest.fixture
def mock_supabase_account_success():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.return_value.data = [MOCK_ACCOUNT]
        yield mock

@pytest.fixture
def mock_supabase_account_error():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.side_effect = Exception("Database error")
        yield mock

# GET Account Balance
@pytest.fixture
def mock_supabase_account_balance_get_success():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [MOCK_ACCOUNT_BALANCE]
        yield mock

@pytest.fixture
def mock_supabase_account_balance_get_error():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.side_effect = Exception("Database error")
        yield mock

@pytest.fixture
def mock_supabase_account_balance_not_found_error():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = []
        yield mock

# Update Account Balance
@pytest.fixture
def mock_supabase_account_balance_update_success():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [MOCK_ACCOUNT_BALANCE]
        mock.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value.data = [MOCK_UPDATED_ACCOUNT_BALANCE]
        yield mock

@pytest.fixture
def mock_supabase_account_balance_update_error():
    with patch('app.services.account_service.supabase') as mock:
        mock.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [MOCK_ACCOUNT_BALANCE]
        mock.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.side_effect = Exception("Database error")
        yield mock

# Create Transfer
@pytest.fixture
def mock_supabase_create_transfer_success():
    with patch('app.services.transfer_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.return_value.data = [MOCK_TRANSFER_SUCCESS]
        yield mock

@pytest.fixture
def mock_supabase_create_transfer_database_error():
    with patch('app.services.transfer_service.supabase') as mock:
        mock.table.return_value.insert.return_value.execute.side_effect = Exception("Database error")
        yield mock
