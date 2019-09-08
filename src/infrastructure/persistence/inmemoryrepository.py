from src.contracts.repository.repository import Repository
from src.domain.model.model import Model
from time import time
import uuid

class InMemoryRepository(Repository):
    def __init__(self):
        # id-indexed in-memory database
        self.dbSet = {}

    def add(self, entity):
        ''' Adds a _new_ entity to the dbSet.

            Keyword arguments:
            entity -- An object that derives type Model and contains an _id_ property
        
            Returns:
            The number of altered rows
        '''
        assert issubclass(type(entity), Model), '{} entity must be of type \'Model\''.format(entity)
        if entity.id in self.dbSet:
            return 0

        entity.id = uuid.uuid4()
        entity.created_at = time()
        self.dbSet[entity.id] = entity

        return 1

    def getByFilter(self, filterExpression):
        ''' Returns entities based on a filterExpression

            Keyword arguments:
            filterExpression -- a function containing a Model-based filter expression
        
            Returns:
            the entities found for the particular expression
        '''
        entities = list(filter(filterExpression, self.dbSet.values()))
        return entities
        
    def getById(self, id):
        ''' Returns the entity from a determined Id

            Keyword arguments:
            id -- a unique id (uuid4)
        
            Returns:
            the entities found for the particular expression
        '''
        try:
            entity = self.dbSet[id]
            return entity
        except:
            return
