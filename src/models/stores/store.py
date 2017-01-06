import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors

class Store(object):
    def __init__(self,name,url_prefix,tag_name,query,_id=None):
        self.name=name
        self.url_prefix=url_prefix
        self.tag_name=tag_name
        self.query=query
        self._id=uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "name":self.name,
            "url_prefix":self.url_prefix,
            "tag_name":self.tag_name,
            "query":self.query,
            "_id":self._id
        }

    @classmethod
    def get_store_by_id(cls,_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{"_id":_id}))

    @classmethod
    def get_store_by_name(cls,name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": name}))

    @classmethod
    def get_store_by_url_prefix(cls,url_prefix):
        """
        url->http://www.johnlewis.com/item/prefix
        h->?
        ht->?
        htt->?
        .
        .
        .
        http://www.jo->Store()
        :param url_prefix:
        :return:
        """
        return cls(**Database.find_one(StoreConstants.COLLECTION, query={"url_prefix":{"$regex": '^{}'.format(url_prefix)}}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION,{'_id':self._id},self.json())


    @classmethod
    def get_by_url(cls,url):
        for i in range(0,len(url)+1):
            s=url[:i]
            try:
                store=cls.get_store_by_url_prefix(s)
                return store
            except:
                raise StoreErrors.StoreNotFound("This store was not found!")

    @classmethod
    def get_stores(cls):
        return [cls(**elem) for elem in Database.find_all(StoreConstants.COLLECTION,{})]

    def delete_store(self):
        Database.remove(StoreConstants.COLLECTION,{'_id':self._id})