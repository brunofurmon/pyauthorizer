from src.contracts.cqrs.commandhandler import CommandHandler
from src.domain.commands.account.createaccount import CreateAccount

class AccountCommandHandler(CommandHandler):
    def __init__(self):
        self.commandHandlerFuncNames = [
            # Add more handlers here whenever necessary
            'CreateAccount'
        ]

    def handle_CreateAccount(self, command):
        assert isinstance(command, CreateAccount), '{} must be of type \'CreateAccount\''.format(command)

        print('{} handled!!!'.format(command))
    