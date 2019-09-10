import unittest
import json
from src.domain.commands.account.createaccount import CreateAccount
from src.domain.model.account import Account 

class CreateAccountTests(unittest.TestCase):
    
    def test_JsonParseAccount_ok(self):
        jsonStr = '{ "account": { "activeCard": true, "availableLimit": 100 } }'

        expected = Account(True, 100)

        result = CreateAccount.parseAccountCreation(jsonStr)

        self.assertDictEqual(expected.toDict(), result.toDict())

    def test_CreateAccountCtor_ok(self):
        jsonStr = '{ "account": { "activeCard": true, "availableLimit": 100 } }'

        expected = Account(True, 100)

        result = CreateAccount(jsonStr)

        self.assertDictEqual(expected.toDict(), result.accountToCreate.toDict())
