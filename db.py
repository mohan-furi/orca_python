import pymongo
from config import config


class DB:
    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb://localhost:27017")
        db_name = config.get('database')
        self.db = self.conn[db_name]
        collections = self.db.list_collection_names()

        table_names = config.get('tables')
        missing_tables = set(table_names).difference(set(collections))
        print('================missing tables', missing_tables)
        for m_table in missing_tables:
            self.db.create_collection(m_table)
        self.create_admin_user()

    def create_admin_user(self):
        admin = self.db['users'].find_one({'email': 'admin'})
        if not admin:
            print('---------No admin user found. Creating one!---------')
            self.db['users'].insert_one(
                {'email': 'admin', 'password': 'admindevx22'})
