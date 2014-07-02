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

    def test_modelize_queries(self):
        with self.app.app_context():

            class TestModel1(self.modelize.Model):
                __collection_name__ = 'test1'
                __type_identifier__ = {'type': 'いち'}
                __fields__ = ['name', 'age']

            class TestModel2(self.modelize.Model):
                __collection_name__ = 'test1'
                __type_identifier__ = {'type': 'に'}
                __fields__ = ['color', 'shape']

            model11 = TestModel1(name='完犊子', age=250)
            model12 = TestModel1(name='狗史', age=38)
            model21 = TestModel2(color='红', shape='S形')
            model22 = TestModel2(color='黄', shape='B形')
            TestModel1.query.insert(model11)
            TestModel1.query.insert(model12)
            TestModel2.query.insert(model21)
            TestModel2.query.insert(model22)


    def tearDown(self):
        pass