class Account(object):    
    def __init__(self, activeCard, availableLimit):
        self.id = None
        self.created_at = None
        self.activeCard = activeCard
        self.availableLimit = availableLimit
    
    def __repr__(self):
        return 'Account(id={}): created_at: {} - Card: {}, Limit: {}'.format(
            self.id,
            self.created_at,
            'Active' if self.activeCard else 'Not Active', 
            self.availableLimit)
