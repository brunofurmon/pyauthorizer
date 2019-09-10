import unittest

from src.domain.commandhandlers.account.accountcommandhandler import AccountCommandHandler
from src.domain.commands.account.createaccount import CreateAccount
from src.domain.model.account import Account
from src.infrastructure.persistence.inmemoryrepository import InMemoryRepository

class AccountCommandHandlerTests(unittest.TestCase):

    # helpers:
    def assertRaisesWithMessage(self, exceptionType, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.fail()

        except exceptionType as inst:
            self.assertEqual(str(inst), msg)

    def test_AccountCommandHandlerCtor_ok(self):

        repository = InMemoryRepository()

        commandHandler = AccountCommandHandler(repository)

        self.assertEqual(repository, commandHandler.accountRepository)
        self.assertEqual(['CreateAccount'], commandHandler.commandHandlerFuncNames)

    def test_AccountCommandHandlerCtor_nok(self):

        repository = object()

        def createAccountCommandHandler():
            AccountCommandHandler(repository) 

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be of type \'Repository\''.format(repository),
            createAccountCommandHandler)

    def test_handleCreateAccount_ok(self):

        repository = InMemoryRepository()
        commandHandler = AccountCommandHandler(repository)
        command = CreateAccount('{ "account": { "activeCard": true, "availableLimit": 100 } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 100 }, "violations": [] }
        expectedAccount = { "account": { "activeCard": True, "availableLimit": 100 }}

        result = commandHandler.handle_CreateAccount(command)

        self.assertEqual(expectedResult, result)

        resultAccount = repository.getByFilter(lambda _: True)[0].toDict()
        self.assertDictEqual(resultAccount, expectedAccount)

    def test_handleCreateAccount_NotAnInstance(self):

        repository = InMemoryRepository()
        commandHandler = AccountCommandHandler(repository)
        command = object()

        def handleCreateAccountFunc():
            commandHandler.handle_CreateAccount(command) 

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be of type \'CreateAccount\''.format(command),
            handleCreateAccountFunc)
    
    def test_handleCreateAccount_AlreadyInitialized(self):

        repository = InMemoryRepository()
        repository.add(Account(True, 42))
        commandHandler = AccountCommandHandler(repository)
        command = CreateAccount('{ "account": { "activeCard": true, "availableLimit": 100 } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 42 }, "violations": ["account-already-initialized"] }

        result = commandHandler.handle_CreateAccount(command) 

        self.assertDictEqual(expectedResult, result)

        emptyResults = repository.getByFilter(lambda account: account.availableLimit == 100)
        self.assertListEqual([], emptyResults)
