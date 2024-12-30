MOCK_CUSTOMER = {
    "id": 1,
    "name": "Test Customer"
}

MOCK_ACCOUNT = {
    "id": 1,
    "name": "Test Account",
    "customer_id": 1,
    "balance": 100.00,
    "account_number": "111111111111",
    "routing_number": "999999999"
}

MOCK_ACCOUNT_BALANCE = {
    "balance": 100.00
}

MOCK_UPDATED_ACCOUNT_BALANCE = {
    "balance": 75.00
}

MOCK_TRANSFER_SUCCESS = {
    "id": 1,
    "sending_account_number": "111111111111",
    "sending_routing_number": "999999999",
    "receiving_account_number": "222222222222",
    "receiving_routing_number": "777777777",
    "transfer_amount": "10",
    "status": "Success"
}

MOCK_TRANSFER_FAILED = {
    "id": 1,
    "sending_account_number": "111111111111",
    "sending_routing_number": "999999999",
    "receiving_account_number": "222222222222",
    "receiving_routing_number": "777777777",
    "transfer_amount": "10",
    "status": "Failed"
}