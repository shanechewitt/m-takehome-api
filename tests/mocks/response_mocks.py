MOCK_CUSTOMER = {
    "id": 1,
    "name": "Test Customer"
}

MOCK_CUSTOMER_LIST = [
    {
        "id": 1,
        "name": "Test Customer 1"
    },
    {
        "id": 2,
        "name": "Test Customer 2"
    },
    {
        "id": 3,
        "name": "Test Customer 3"
    }
]

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

MOCK_TRANSFER_HISTORY = [
    {
        "sending_account_number": "111111111111",
        "receiving_account_number": "222222222222",
        "transfer_amount": "10.05",
        "status": "Success"
    },
    {
        "sending_account_number": "333333333333",
        "receiving_account_number": "111111111111",
        "transfer_amount": "100.05",
        "status": "Failed: Insufficient Funds"
    },
    {
        "sending_account_number": "111111111111",
        "receiving_account_number": "6666666666666",
        "transfer_amount": "10.05",
        "status": "Success"
    },
]