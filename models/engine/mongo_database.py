#!/usr/bin/python3

import pymongo
import re
from settings.loadenv import handleEnv
from datetime import datetime, timedelta
from bson import ObjectId

classes = {"vehicles": "Vehicle", "users": "User", "devices": "Device",
           "usersession": "UserSession"}


class Database:
    all_objs = {}

    def __init__(self):
        db_name = handleEnv('DB_NAME')
        url = handleEnv('HOST')

        try:
            self.client = pymongo.MongoClient(url)
            self.db = self.client[db_name]
        except Exception as e:
            print("Unable to connect to mongo server:", e)

    def all(self, cls=None):
        if cls and cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls and cls not in classes:
            try:
                cls = cls.__tablename__
            except Exception as e:
                raise ValueError('Invalid search parameter')
        if cls:
            new_dict = {key: obj for key, obj in self.all_objs.items() if obj.__tablename__ == cls}
            return new_dict
        return self.all_objs

    def save(self, model):
        """
        Save a new document in the specified collection.
        Args:
            model (class): The model class representing the collection.
        """
        if not model:
            return
        query = {'id': model.id}
        vals = model.to_dict()
        if '_id' in vals and isinstance(vals['_id'], str):
            vals['_id'] = ObjectId(vals['_id'])
        new_attrs = {"$set": vals}
        self.db[model.__tablename__].update_one(query, new_attrs, upsert=True)
        self.all_objs[f'{model.to_dict().get("__class__")}.{model.id}'] = model

    def delete(self, model):
        """
        Remove a document from the specified collection based on a query.
        Args:
            model (class): The instance representing the document.
        """
        try:
            result = self.db[model.__tablename__].delete_one({'id': model.id})
            del self.all_objs[f'{model.to_dict().get("__class__")}.{model.id}']
            print(f'{result.deleted_count} document(s) deleted successfully.')
        except pymongo.errors.PyMongoError as e:
            print(f'Error deleting document(s): {e}')
        except Exception as e:
            print(f'Error deleting document: {e}')

    def close(self):
        self.reload()

    def reload(self):
        """This recreates all objects and save them to __objects"""
        from models.user import User
        from models.vehicle import Vehicle

        classes2 = {'User': User, 'Vehicle': Vehicle}

        try:
            for cls in classes:
                models = self.db[cls].find()
                for obj in list(models):
                    model = classes2[obj['__class__']](**obj)
                    key = f"{model.__class__.__name__}.{model.id}"
                    self.all_objs[key] = model
        except Exception as e:
            print(e)
            pass

    def get(self, cls, id):
        if cls in classes:
            cls = classes[cls]
        elif not isinstance(cls, str):
            try:
                cls = cls.__class__
            except Exception as e:
                raise("Invalid parameter for get function")
        key = f"{cls}.{id}"
        
        obj = self.all_objs.get(key, None)
        if obj and obj.__class__ == 'UserSession':
            if datetime.now() > obj.created_at + timedelta(hours=72):
                self.delete(obj)
                return
        return obj

    def search(self, cls, **kwargs):
        """This filters the storage for objects matching kwargs
        Args:
            cls (str): The class to search for the documents
            kwargs (dict): filter parameters
        Return:
            A list of documents matching the description
        """
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            try:
                cls = cls.__tablename__
            except Exception as e:
                raise ValueError('Invalid search parameter')

        case_insensitive_kwargs = {
                key: {'$regex': re.escape(value), '$options': 'i'} if isinstance(value, str) else value
                for key, value in kwargs.items()
                }
        
        pipeline = []
        match_stage = {
            '$match': {
                '$and': [
                    case_insensitive_kwargs
                ]
            }
        }
        pipeline.append(match_stage)
        docs = self.db[cls].aggregate(pipeline)

        result = []
        if docs:
            for doc in docs:
                key = doc['__class__'] + "." + doc['id']

                model = self.all_objs[key]
                result.append(model)
        return result
    
    def count(self, cls, key=None):
        """This counts the number of documents in a cls,
            If key is provided, it sums all the values of that key in the collection
        Args:
            cls (str): the class name or collection
            key (str): [optional] key containing the field to count
        Return:
            int: count of found documents
        """
        if cls not in classes:
            for k, v in classes.items():
                if v == cls:
                    cls = k
                    break
        if cls not in classes:
            cls = cls.__tablename__

        return self.db[cls].count_documents({})

    def paginate_query(self, cls, pgnum, pgsize, **kwargs):
        """This handles pagination by returning limited data
        Args:
            cls (str): the collection name or class
            pgnum (int): the page number
            pgsize (int): the items to return per page
        Return:
            a list of requested items"""
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__
        pgnum = int(pgnum)
        pgsize = int(pgsize)

        if not kwargs:
            result = []
            try:
                offset = (int(pgnum) - 1) * int(pgsize)
                documents = self.db[cls].find().skip(offset).limit(pgsize)
                for document in documents:
                    model = self.reload(document['__class__'], **document)
                    result.append(model)
                return result
            except Exception as e:
                print(e)
                return result
        else:
            result = []
            try:
                offset = (int(pgnum) - 1) * int(pgsize)
                documents = self.db[cls].find( kwargs ).skip(offset).limit(pgsize)
                for document in documents:
                    model = self.reload(document['__class__'], **document)
                    result.append(model)
                return result
            except Exception as e:
                print(e)
                return result

    def search_paginate(self, cls, pgnum, pgsize, **kwargs):
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        try:
            offset = (int(pgnum) - 1) * int(pgsize)
            result = self.db[cls].find( kwargs ).skip(offset).limit(pgsize)
            return result
        except Exception as e:
            print(e)
            return []
        
    def listFilter(self, cls, **kwargs):
        """
        Filter the collection based on a dictionary of filter parameters.
        Args:
            cls (class): The model class representing the collection.
            kwargs (dict): A dictionary of filter parameters where values can be lists.
        Returns:
            list: A list of filtered documents.
        """
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        result = []
        try:
            query = {}
            for key, values in kwargs.items():
                if key == 'max_price' and 'min_price' in kwargs.items():
                    query['price'] = {"$gte": kwargs['min_price'], "$lte": values}
                elif key == 'min_price' and 'max_price' in kwargs:
                    query['price'] = {"$gte": values, "$lte": kwargs['max_price']}
                elif isinstance(values, list):
                    query[key] = {"$in": values}
                elif key != 'max_price' and key != 'min_price':
                    query[key] = values
            # query = {key: {"$in": values} if isinstance(values, list) else values
            #          for key, values in kwargs.items()}
            documents = self.db[cls].find(query)
            for document in documents:
                model = self.reload(document['__class__'], **document)
                result.append(model)
            return result
        except pymongo.errors.PyMongoError as e:
            print(f'Error performing list filter: {e}')
            return []

    def sort_limit(self, cls, limit):
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        objs = self.db[cls].find().sort("no_clicks", -1).limit(limit)
        result = []
        for obj in objs:
            model = self.reload(obj['__class__'], **obj)
            result.append(model)
        return result
