import json
from src.domain.model.transaction import Transaction
from src.contracts.cqrs.command import Command

class AuthorizeTransaction(Command):
    def __init__(self, line):
        self.transactionToCreate = AuthorizeTransaction.parseTransactionAuthorization(line)
    
    @staticmethod
    def parseTransactionAuthorization(line):
        ''' Parses an AuthorizeTransaction command arguments

            Keyword arguments:
                line -- JSON operation line containing "merchant": string, "amount": int and "time": ISO time
            
            Returned Value:
                Transaction -- Transaction object built with the fields from the operation
        '''
        fieldsDict = json.loads(line)['transaction']

        transaction = Transaction(
            fieldsDict['merchant'],
            fieldsDict['amount'],
            fieldsDict['time'])

        return transaction


        
