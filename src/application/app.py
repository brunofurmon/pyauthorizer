import sys

from src.domain.commands.account.createaccount import CreateAccount
from src.domain.commands.account.createaccount import CreateAccount
from src.domain.commandhandlers.account.accountcommandhandler import AccountCommandHandler
from src.domain.commandhandlers.transaction.transactioncommandhandler import TransactionCommandHandler
from src.infrastructure.bus.inmemorycommandbus import InMemoryCommandBus
from src.infrastructure.bus.inmemoryquerybus import InMemoryQueryBus

# Command Bus Setup
commandBus = InMemoryCommandBus()

commandBus.subscribe(AccountCommandHandler())
# commandBus.subscribe(TransactionCommandHandler())

# Query Bus Setup
queryBus = InMemoryQueryBus()

def getCommandFromJson(line):
    ''' Dispatches the current @line command

    Keyword arguments:
        line -- JSON formatted line containing an operation
    '''
    command = None

    # Processing an account
    if '"account"' in line:
        command = CreateAccount(line)
        print("I'll process an account: {}".format(command.accountToCreate))

    # Transaction
    else:
        print("I'll process a transaction", line)
        # command = CreateTransaction
    
    return command

def main():
    # Operates each line from STDIN. Supposing the program is called as following:
    # python ./src/application/app.py < operations
    for line in sys.stdin:
        command = getCommandFromJson(line)

        response = commandBus.send(command)
        print(response)

if __name__ == '__main__':
    main()