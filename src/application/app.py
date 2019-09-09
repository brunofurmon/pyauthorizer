import sys
import os

sys.path.append('./')

import json

from src.domain.commands.account.createaccount import CreateAccount
from src.domain.commands.transaction.authorizetransaction import AuthorizeTransaction
from src.domain.commandhandlers.account.accountcommandhandler import AccountCommandHandler
from src.domain.commandhandlers.transaction.transactioncommandhandler import TransactionCommandHandler

from src.infrastructure.bus.inmemorycommandbus import InMemoryCommandBus
from src.infrastructure.bus.inmemoryquerybus import InMemoryQueryBus
from src.infrastructure.persistence.inmemoryrepository import InMemoryRepository

def getCommandFromJson(line):
    ''' Dispatches the current @line command

    Keyword arguments:
        line -- JSON formatted line containing an operation
    '''
    command = None

    # Processing an account
    if '"account"' in line:
        command = CreateAccount(line)

    # Transaction
    else:
        command = AuthorizeTransaction(line)
    
    return command

def main():
    # Operates each line from STDIN. Supposing the program is called as following:
    # python ./src/application/app.py < operations
    
    # Repository Setup
    accountRepository = InMemoryRepository()
    transactionRepository = InMemoryRepository()

    # Command Bus Setup
    commandBus = InMemoryCommandBus()

    accountCommandsHandler = AccountCommandHandler(accountRepository)
    commandBus.subscribe(accountCommandsHandler)

    transactionCommandsHandler = TransactionCommandHandler(transactionRepository, accountRepository)
    commandBus.subscribe(transactionCommandsHandler)

    # Main loop
    for line in sys.stdin:
        command = getCommandFromJson(line)

        result = commandBus.send(command)
        output = json.dumps(result)

        print(output)

if __name__ == '__main__':
    main()