import unittest
from src.domain.model.account import Account

class AccountTests(unittest.TestCase):

    def test_getAccountAndViolationsDict_empty(self):
        account = Account(True, 100)
        violations = []

        expectedDict = { "account": { "activeCard": True, "availableLimit": 100 }, "violations": [] }
        result = Account.getAccountAndViolationsDict(account, violations)

        self.assertDictEqual(expectedDict, result)

    def test_getAccountAndViolationsDict_Valid(self):
        account = Account(True, 99)
        violations = ['insufficient-limit']

        expectedDict = { "account": { "activeCard": True, "availableLimit": 99 }, "violations": ['insufficient-limit'] }
        result = Account.getAccountAndViolationsDict(account, violations)

        self.assertDictEqual(expectedDict, result)
