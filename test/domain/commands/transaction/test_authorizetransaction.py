import unittest
import json
from src.domain.model.transaction import Transaction
from src.domain.commands.transaction.authorizetransaction import AuthorizeTransaction

class AuthorizeTransactionTests(unittest.TestCase):
    
    def test_JsonParseTransaction_ok(self):
        jsonStr = '{ "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:02:00.000Z" } }'

        expected = Transaction("Burger King", 10, "2019-02-13T10:02:00.000Z")

        result = AuthorizeTransaction.parseTransactionAuthorization(jsonStr)

        self.assertEqual(expected.amount, result.amount)
        self.assertEqual(expected.merchant, result.merchant)
        self.assertEqual(expected.time, result.time)

    def test_AuthorizeTransactionCtor_ok(self):
        jsonStr = '{ "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:02:00.000Z" } }'

        expected = Transaction("Burger King", 10, "2019-02-13T10:02:00.000Z")

        result = AuthorizeTransaction(jsonStr)

        self.assertEqual(expected.amount, result.transactionToCreate.amount)
        self.assertEqual(expected.merchant, result.transactionToCreate.merchant)
        self.assertEqual(expected.time, result.transactionToCreate.time)