import sys
import json

from src.domain.commands.account.createaccount import CreateAccount
from src.domain.commands.account.createaccount import CreateAccount
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
        # command = CreateTransaction
        pass
    
    return command

def main():
    # Operates each line from STDIN. Supposing the program is called as following:
    # python ./src/application/app.py < operations
    
    # Repository Setup
    accountRepository = InMemoryRepository()

    # Command Bus Setup
    commandBus = InMemoryCommandBus()

    accountCommandsHandler = AccountCommandHandler(accountRepository)
    commandBus.subscribe(accountCommandsHandler)
    # commandBus.subscribe(TransactionCommandHandler())

    # Query Bus Setup
    queryBus = InMemoryQueryBus()

    for line in sys.stdin:
        command = getCommandFromJson(line)

        violations = commandBus.send(command)

        output = json.loads(line)

        if violations:
            output.update({'violations': violations})
        
        print(output)

if __name__ == '__main__':
    main()