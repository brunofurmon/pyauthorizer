from datetime import datetime, timedelta

from src.contracts.cqrs.commandhandler import CommandHandler
from src.contracts.repository.repository import Repository
from src.domain.commands.transaction.authorizetransaction import AuthorizeTransaction

class TransactionCommandHandler(CommandHandler):
    def __init__(self, transactionRepository, accountRepository):
        assert isinstance(transactionRepository, Repository), '{} must be of type \'Repository\''.format(transactionRepository)
        assert isinstance(accountRepository, Repository), '{} must be of type \'Repository\''.format(accountRepository)

        self.commandHandlerFuncNames = [
            # Add more handlers here whenever necessary
            'AuthorizeTransaction'
        ]

        self.transactionRepository = transactionRepository
        self.accountRepository = accountRepository

    def handle_AuthorizeTransaction(self, command):
        ''' Handles AuthorizeTransaction command

            Keyword Arguments:
            command -- Command entity with necessary transaction authorization data

            Returns:
            A dictionary containing the account and a new field containing possible violations
        '''
        assert isinstance(command, AuthorizeTransaction), '{} must be of type \'AuthorizeTransaction\''.format(command)

        transaction = command.transactionToCreate
        violations = []

        # Gets the first account
        account = self.accountRepository.getByFilter(lambda account: True)[0]

        # •	No transaction should be accepted when the card is not active: card-not-active
        if not account.activeCard:
            violations += ['card-not-active']
            return TransactionCommandHandler.getAccountAndViolationsDict(account, violations)

        # •	The transaction amount should not exceed available limit: insufficient-limit
        if account.availableLimit < transaction.amount:
            violations += ['insufficient-limit']
            return TransactionCommandHandler.getAccountAndViolationsDict(account, violations)

        # •	There should not be more than 3 transactions on a 2 minute interval: high-frequency-small-interval
        transactionTime = datetime.strptime(transaction.time, '%Y-%m-%dT%H:%M:%S.%fZ')

        minDiffInMinutes = 2
        fromDatetime = transactionTime - timedelta(minutes=minDiffInMinutes)

        recentTransactions = self.transactionRepository.getByFilter(lambda transaction: transaction.time >= fromDatetime )
        
        if len(recentTransactions) > 3:
            violations += ['high-frequency-small-interval']
            return TransactionCommandHandler.getAccountAndViolationsDict(account, violations)

        # •	There should not be more than 2 similar transactions (same amount and merchant) in a 2 minutes interval: doubled-transaction
        doubledTransactions = list(filter(lambda transaction: \
            transaction.amount == transaction.amount \
            and transaction.merchant == transaction.merchant \
            , recentTransactions))

        if doubledTransactions and doubledTransactions > 1:
            violations += ['doubled-transaction']
            return TransactionCommandHandler.getAccountAndViolationsDict(account, violations)

        # Everything should be fine down here
        self.transactionRepository.add(transaction)

        account.availableLimit -= transaction.amount
        self.accountRepository.update(account)

        return TransactionCommandHandler.getAccountAndViolationsDict(account, violations)

    @staticmethod
    def getAccountAndViolationsDict(account, violations):
        returnDict = account.toDict()
        returnDict.update({'violations': violations})

        return returnDict
