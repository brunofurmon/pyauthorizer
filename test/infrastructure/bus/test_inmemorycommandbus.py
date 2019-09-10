import unittest

from src.infrastructure.bus.inmemorycommandbus import InMemoryCommandBus
from src.contracts.cqrs.commandhandler import CommandHandler 
from src.contracts.cqrs.command import Command 

class InMemoryCommandBusTests(unittest.TestCase):
    
    # helpers:
    def assertRaisesWithMessage(self, exceptionType, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.fail()

        except exceptionType as inst:
            self.assertEqual(str(inst), msg)
    
    def test_Subscribe_ok(self):

        class TestHandler(CommandHandler):
            def __init__(self):
                self.commandHandlerFuncNames = ['TestFunc']
            def handle_TestFunc(self):
                pass

        bus = InMemoryCommandBus()
        handler = TestHandler()

        bus.subscribe(handler)

        self.assertTrue(callable(bus._TestFunc_handler))
    
    def test_Subscribe_NotCallable(self):

        class TestHandler(CommandHandler):
            def __init__(self):
                self.commandHandlerFuncNames = ['TestFunc']
                self.handle_TestFunc = ''

        bus = InMemoryCommandBus()
        handler = TestHandler()

        def trySubscribingBadHandler():
            bus.subscribe(handler)

        self.assertRaisesWithMessage(
            AssertionError,
            '{} must be callable'.format(handler.handle_TestFunc),
            trySubscribingBadHandler
        )
    
    def test_Send_ok(self):

        class TestHandler(CommandHandler):
            def __init__(self):
                self.commandHandlerFuncNames = ['TestFunc']
                self.verified = False
            def handle_TestFunc(self, command):
                self.verified = True

        class TestFunc(Command):
            pass

        bus = InMemoryCommandBus()
        handler = TestHandler()
        bus.subscribe(handler)
        command = TestFunc()

        bus.send(command)

        self.assertTrue(callable(bus._TestFunc_handler))
        self.assertTrue(handler.verified)

    def test_Send_NotSubscribed(self):

        class TestHandler(CommandHandler):
            def __init__(self):
                self.commandHandlerFuncNames = ['TestFunc']
                self.verified = False
            def handle_TestFunc(self, command):
                self.verified = True

        class TestFunc(Command):
            pass

        bus = InMemoryCommandBus()
        handler = TestHandler()
        
        command = TestFunc()

        def trySendingUnsubscribedHandler():
            bus.send(command)

        self.assertRaisesWithMessage(
            NotImplementedError,
            '_TestFunc_handler is not implemented. Did you remember to subscribe?',
            trySendingUnsubscribedHandler
        )
