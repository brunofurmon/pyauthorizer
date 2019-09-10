import unittest
import uuid

from src.infrastructure.persistence.inmemoryrepository import InMemoryRepository
from src.domain.model.model import Model

class InMemoryRepositoryTests(unittest.TestCase):

    # helpers:
    def assertRaisesWithMessage(self, exceptionType, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.fail()

        except exceptionType as inst:
            self.assertEqual(str(inst), msg)
    
    def test_RepoCtor_ok(self):
        repo = InMemoryRepository()

        self.assertDictEqual({}, repo.dbSet)
    
    def test_RepoAdd_ok(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        rowsAffected = repo.add(model)

        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertEqual(1, len(repo.dbSet))
        self.assertEqual(1, rowsAffected)
    
    def test_RepoAdd_NotModelInstance(self):
        repo = InMemoryRepository()

        model = object()

        def tryAddingNotModelInstance():
            repo.add(model)

        self.assertRaisesWithMessage(
            AssertionError,
            '{} entity must be of type \'Model\''.format(model),
            tryAddingNotModelInstance
        )
    
    def test_RepoAdd_Existing(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        rowsAffected = repo.add(model)
        self.assertEqual(1, rowsAffected)

        rowsAffected = repo.add(model)

        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertEqual(1, len(repo.dbSet))
        self.assertEqual(0, rowsAffected)
    
    def test_RepoGetByFilter_ok(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        repo.add(model)

        result = repo.getByFilter(lambda x: x.id == model.id)

        self.assertListEqual([model], result)
    
    def test_RepoGetByFilter_NotFound(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        repo.add(model)

        result = repo.getByFilter(lambda x: False)

        self.assertListEqual([], result)
    
    def test_RepoGetById_ok(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        repo.add(model)

        result = repo.getById(model.id)

        self.assertEqual(model, result)

    def test_RepoGetById_NotFound(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                super().__init__()

        model = TestModel()

        repo.add(model)

        result = repo.getById(uuid.uuid4())

        self.assertIsNone(result)
    
    def test_RepoUpdate_ok(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                self.verified = False
                super().__init__()

        model = TestModel()

        repo.add(model)
        self.assertIsNone(model.updated_at)
        self.assertFalse(model.verified)

        model.verified = True
        affectedRows = repo.update(model)
        self.assertEqual(1, affectedRows)

        updatedModel = repo.getById(model.id)
        self.assertIsNotNone(updatedModel.updated_at)
        self.assertTrue(updatedModel.verified)
    
    def test_RepoUpdate_NotFound(self):
        repo = InMemoryRepository()

        class TestModel(Model):
            def __init__(self):
                self.verified = False
                super().__init__()

        model = TestModel()

        repo.add(model)
        self.assertIsNone(model.updated_at)
        self.assertFalse(model.verified)

        newModel = Model()
        affectedRows = repo.update(newModel)
        self.assertEqual(0, affectedRows)

        notUpdatedModel = repo.getById(model.id)
        self.assertIsNone(notUpdatedModel.updated_at)
        self.assertFalse(notUpdatedModel.verified)
