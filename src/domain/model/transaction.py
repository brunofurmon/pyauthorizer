from src.domain.model.model import Model

class Transaction(Model):
    def __init__(self, merchant, amount, time):
        super().__init__()
        self.merchant = merchant
        self.amount = amount
        self.time = time
        
    def __repr__(self):
        return 'Transaction(id={}): created_at: {} - Merchant: {}, Amount: {}, Time: {}'.format(
            self.id,
            self.created_at,
            self.merchant, 
            self.amount,
            self.time)
            