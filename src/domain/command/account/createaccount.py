import json
from src.domain.model.account import Account

class CreateAccount(object):
    def __init__(self, line):
        self.accountToCreate = CreateAccount.parseAccountCreation(line)
    
    @staticmethod
    def parseAccountCreation(line):
        ''' Parses an AccountCreation command arguments

            Keyword arguments:
                line -- JSON operation line containing "activeCard": boolean and "availableLimit": Integer
            
            Returned Value:
                account -- Account object built with the fields from the operation
        '''
        fieldsDict = json.loads(line)['account']

        account = Account(fieldsDict['activeCard'], fieldsDict['availableLimit'])

        return account


        
