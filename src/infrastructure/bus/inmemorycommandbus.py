from src.contracts.cqrs.command import Command
from src.contracts.bus.commandbus import CommandBus

class InMemoryCommandBus(CommandBus):
    def __init__(self):
        pass
    
    def subscribe(self, handler):
        # Gets all handle_* functions and addresses into the bus.
        for commandHandlerFuncName in handler.commandHandlerFuncNames:
            handlerFuncName = 'handle_{}'.format(commandHandlerFuncName)

            func = getattr(handler, handlerFuncName)

            assert callable(func), '{} must be a callable'.format(func.__name__)

            setattr(self, '_{}_handler'.format(commandHandlerFuncName), func)

    def send(self, command):
        assert isinstance(command, Command), '{} should be of type \'Command\''.format(command)

        try:
            handlerFunc = getattr(self, '_{}_handler'.format(type(command).__name__))
        except:
            raise NotImplementedError('_{}_handler is not implemented. Did you remember to subscribe?'.format(type(command).__name__))

        return handlerFunc(command)
