import pymongo

class Database(object):
    URI='mongodb://127.0.0.1:27017'
    DATABASE=None

    @staticmethod
    def initialize():
        client=pymongo.MongoClient(Database.URI)
        Database.DATABASE=client['fullstack']

    @staticmethod
    def insert(collection,query):
        Database.DATABASE[collection].insert(query)

    @staticmethod
    def find_all(collection,query):
        data=Database.DATABASE[collection].find(query)
        return data

    @staticmethod
    def find_one(collection,query):
        data=Database.DATABASE[collection].find_one(query)
        return data

    @staticmethod
    def update(collection,query,data):
        Database.DATABASE[collection].update(query,data,upsert=True)# upsert if no element with query found then insert into database

    @staticmethod
    def remove(collection, query):
        data = Database.DATABASE[collection].remove(query)