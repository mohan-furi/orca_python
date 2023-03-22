from db import DB
from bson.objectid import ObjectId


class BaseApi(DB):
    def __init__(self):
        super().__init__()

    def find_one(self, table, query={}, fields_except=[]):
        except_filter = {field: 0 for field in fields_except}
        print(query, except_filter)
        res = self.db[table].find_one(query, except_filter)
        return res

    def find_all(self, table, filter_by={}, fields_except=[]):
        except_filter = {field: 0 for field in fields_except}
        cursor = self.db[table].find(filter_by, except_filter)
        res = [cur for cur in cursor]
        for i in range(len(res)):
            res[i]['_id'] = res[i].get('_id').__str__()
        return res

    def insert_one(self, table, data):
        res = self.db[table].insert_one(data)

        return res.inserted_id or False

    def insert_many(self, table, data):
        res = self.db[table].insert_many(list(data))
        return [re.inserted_ids for re in res]

    def delete_one(self, table, ids):
        res = self.db[table].delete_one(filter={'_id':  ObjectId(ids)})
        print(res)
        return True if res else False
