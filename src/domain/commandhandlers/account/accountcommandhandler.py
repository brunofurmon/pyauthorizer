from src.contracts.cqrs.commandhandler import CommandHandler
from src.contracts.repository.repository import Repository
from src.domain.commands.account.createaccount import CreateAccount

class AccountCommandHandler(CommandHandler):
    def __init__(self, accountRepository):
        assert isinstance(accountRepository, Repository), '{} must be of type \'Repository\''.format(accountRepository)

        self.commandHandlerFuncNames = [
            # Add more handlers here whenever necessary
            'CreateAccount'
        ]

        self.accountRepository = accountRepository

    def handle_CreateAccount(self, command):
        ''' Handles CreateAccount command

            Keyword Arguments:
            command -- Command entity with necessary account creation data

            Returns:
            An array containing violations ocurred during execution
        '''
        assert isinstance(command, CreateAccount), '{} must be of type \'CreateAccount\''.format(command)

        violations = []
        account = command.accountToCreate

        existingAccounts = self.accountRepository.getByFilter(lambda account: True)

        if existingAccounts:
            violations += ['account-already-initialized']
            returnDict = AccountCommandHandler.getAccountAndViolationsDict(account, violations)

        self.accountRepository.add(account)

        returnDict = AccountCommandHandler.getAccountAndViolationsDict(account, violations)

        return returnDict
    
    @staticmethod
    def getAccountAndViolationsDict(account, violations):
        returnDict = account.toDict()
        returnDict.update({'violations': violations})

        return returnDict
    