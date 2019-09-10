from src.domain.model.model import Model

class Account(Model):    
    def __init__(self, activeCard, availableLimit):
        super().__init__()
        self.activeCard = activeCard
        self.availableLimit = availableLimit
    
    def __repr__(self):
        return 'Account(id={}): created_at: {} - Card: {}, Limit: {}'.format(
            self.id,
            self.created_at,
            'Active' if self.activeCard else 'Not Active', 
            self.availableLimit)
    
    def toDict(self):
        return { 
            "account": 
            {
                "activeCard": self.activeCard,
                "availableLimit": self.availableLimit 
            }
        }

    @staticmethod
    def getAccountAndViolationsDict(account, violations):
        returnDict = account.toDict()
        returnDict['violations'] = violations

        return returnDict
