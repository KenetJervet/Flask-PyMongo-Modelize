__author__ = 'kj'

import unittest
from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo.database import Database
from tests.testenv import flask_stub_config
from flask_pymongo_modelize import Modelize


class PyMongoUnderstandingTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(flask_stub_config)
        self.mongo = PyMongo(self.app)

    def test_mongo_collection_type(self):
        with self.app.app_context():
            self.assertIsInstance(self.mongo.db, Database)

    def tearDown(self):
        pass


class ModelizeTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(flask_stub_config)
        self.mongo = PyMongo(self.app)
        self.modelize = Modelize(self.mongo)

        class TestBaseModel(self.modelize.Model):
            __collection_name__ = 'test1'
            __fields__ = ['base_1', 'base_2']

        class TestModel1(TestBaseModel):
            __collection_name__ = 'test1'
            __type_identifier__ = {'type': 'いち'}
            __fields__ = ['name', 'age']

        class TestModel2(TestBaseModel):
            __collection_name__ = 'test1'
            __type_identifier__ = {'type': 'に'}
            __fields__ = ['color', 'shape']

        self.TestModel1 = TestModel1
        self.TestModel2 = TestModel2

        with self.app.app_context():
            self.mongo.db.test1.drop()

            model11 = TestModel1(name='完犊子', age=250)
            model12 = TestModel1(name='狗史', age=None)
            model21 = TestModel2(color='红', shape='S形')
            model22 = TestModel2(color='黄', shape='B形')
            TestModel1.query.insert(model11)
            TestModel1.query.insert(model12)
            TestModel2.query.insert(model21)
            TestModel2.query.insert(model22)

    def test_modelize_find_and_find_one(self):
        with self.app.app_context():
            new_model11 = self.TestModel1.query.find_one({'age': 250})
            self.assertIsNotNone(new_model11)
            self.assertIsInstance(new_model11, self.TestModel1)
            self.assertIsNone(new_model11.base_1)
            self.assertEqual(new_model11.name, '完犊子')
            none_model20 = self.TestModel2.query.find_one({'age': 250})
            self.assertIsNone(none_model20)
            models_with_ages = self.TestModel1.query.find({'age': {'$ne': None}})
            self.assertEqual(len(models_with_ages), 1)

    def test_modelize_update(self):
        # TODO: This is crappy. We should use change tracker or something, and
        # the user should be able to simple run update() to flush all changes.

        with self.app.app_context():
            model11 = self.TestModel1.query.find_one({'name': '狗史'})
            self.TestModel1.query.update(model11, {'$set': {'age': 500}})
            model11 = self.TestModel1.query.find_one({'name': '狗史'})
            self.assertEqual(model11.age, 500)

    def tearDown(self):
        pass