import unittest
from datetime import datetime

from src.infrastructure.persistence.inmemoryrepository import InMemoryRepository
from src.domain.model.transaction import Transaction
from src.domain.model.account import Account
from src.domain.commandhandlers.transaction.transactioncommandhandler import TransactionCommandHandler
from src.domain.commands.transaction.authorizetransaction import AuthorizeTransaction

class TransactionCommandHandlerTests(unittest.TestCase):

    # helpers:
    def assertRaisesWithMessage(self, exceptionType, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.fail()

        except exceptionType as inst:
            self.assertEqual(str(inst), msg)

    def test_TransactionCommandHandlerCtor_ok(self):
        transactionRepository = InMemoryRepository()
        accountRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        self.assertEqual(transactionRepository, commandHandler.transactionRepository)
        self.assertEqual(accountRepository, commandHandler.accountRepository)
        self.assertEqual(['AuthorizeTransaction'], commandHandler.commandHandlerFuncNames)

    def test_TransactionCommandHandlerCtor_accountRepo_nok(self):
        transactionRepository = InMemoryRepository()
        accountRepository = object()

        def createAccountCommandHandler():
            TransactionCommandHandler(transactionRepository, accountRepository)

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be of type \'Repository\''.format(accountRepository),
            createAccountCommandHandler)

    def test_TransactionCommandHandlerCtor_transactionRepo_nok(self):
        transactionRepository = object()
        accountRepository = InMemoryRepository()

        def createAccountCommandHandler():
            TransactionCommandHandler(transactionRepository, accountRepository)

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be of type \'Repository\''.format(transactionRepository),
            createAccountCommandHandler)

    def test_handleCreateAccount_ok(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        accountRepository.add(Account(True, 100))

        command = AuthorizeTransaction('{ "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:00:00.000Z" } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 90 }, "violations": [] }
        expectedAccount = { "account": { "activeCard": True, "availableLimit": 90 }}

        result = commandHandler.handle_AuthorizeTransaction(command)

        self.assertEqual(expectedResult, result)

        resultAccount = accountRepository.getByFilter(lambda _: True)[0].toDict()
        self.assertDictEqual(resultAccount, expectedAccount)

    def test_handleCreateAccount_CommandNotAnInstance(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        command = object()

        def handleAuthorizeTransactionFunc():
            commandHandler.handle_AuthorizeTransaction(command) 

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be of type \'AuthorizeTransaction\''.format(command),
            handleAuthorizeTransactionFunc)
    
    def test_handleCreateAccount_CardNotActive(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        accountRepository.add(Account(False, 100))

        command = AuthorizeTransaction('{ "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:00:00.000Z" } }')

        expectedResult = { "account": { "activeCard": False, "availableLimit": 100 }, "violations": ['card-not-active'] }

        result = commandHandler.handle_AuthorizeTransaction(command)

        self.assertEqual(expectedResult, result)

        transactions = transactionRepository.getByFilter(lambda _: True)
        self.assertListEqual([], transactions)
    
    def test_handleCreateAccount_InsufficientLimit(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        accountRepository.add(Account(True, 100))

        command = AuthorizeTransaction('{ "transaction": { "merchant": "Burger King", "amount": 101, "time": "2019-02-13T10:00:00.000Z" } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 100 }, "violations": ['insufficient-limit'] }

        result = commandHandler.handle_AuthorizeTransaction(command)

        self.assertEqual(expectedResult, result)

        transactions = transactionRepository.getByFilter(lambda _: True)
        self.assertListEqual([], transactions)
    
    def test_handleCreateAccount_HighFrequencySmallInterval(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        accountRepository.add(Account(True, 75))
        transactionRepository.add(Transaction("Burger King", 10, datetime.strptime("2019-02-13T11:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')))
        transactionRepository.add(Transaction("Burger Queen", 10, datetime.strptime("2019-02-13T11:01:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')))
        transactionRepository.add(Transaction("Burger Prince", 5, datetime.strptime("2019-02-13T11:01:59.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')))

        command = AuthorizeTransaction('{ "transaction": { "merchant": "Burger Pleb", "amount": 10, "time": "2019-02-13T10:00:00.000Z" } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 75 }, "violations": ['high-frequency-small-interval'] }

        result = commandHandler.handle_AuthorizeTransaction(command)

        self.assertEqual(expectedResult, result)
    
    def test_handleCreateAccount_DoubledTransaction(self):

        accountRepository = InMemoryRepository()
        transactionRepository = InMemoryRepository()

        commandHandler = TransactionCommandHandler(transactionRepository, accountRepository)

        accountRepository.add(Account(True, 75))
        transactionRepository.add(Transaction("Burger King", 10, datetime.strptime("2019-02-13T11:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')))
        transactionRepository.add(Transaction("Burger King", 10, datetime.strptime("2019-02-13T11:01:59.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')))

        command = AuthorizeTransaction('{ "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-02-13T11:02:00.000Z" } }')

        expectedResult = { "account": { "activeCard": True, "availableLimit": 75 }, "violations": ['doubled-transaction'] }

        result = commandHandler.handle_AuthorizeTransaction(command)

        self.assertEqual(expectedResult, result)
    