#!/usr/bin/python3

from models.engine.mongo_database import Database


storage = Database()
storage.reload()
