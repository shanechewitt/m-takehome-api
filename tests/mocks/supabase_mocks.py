import pytest
from unittest.mock import patch
from .response_mocks import MOCK_CUSTOMER

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
        