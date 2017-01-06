import requests
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
import uuid
from bs4 import BeautifulSoup
from src.models.stores.store import Store

class Item(object):
    def __init__(self,name,url,_id=None,price=0.0):
        self.name=name
        store=Store.get_by_url(url)
        self.tag_name=store.tag_name
        self.query=store.query
        self.url=url
        self.price = float(price)
        self._id=_id if _id is not None else uuid.uuid4().hex

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name,self.url)

    def load_price(self):
        request=requests.get(self.url) #get the content from website
        content=request.content # extract the content from the request
        soup=BeautifulSoup(content,"html.parser") # Prepare Soup
        element=soup.find(self.tag_name,self.query) #find the price exact element
        price=element.text.strip() # strip the whitespaces from both sides
        pattern=re.compile('(([\d]+,)*[\d]+\.[\d]+)') # search for this exact pattern using regex e.g. 2,499
        match=pattern.search(price)
        self.price=float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION,{'_id':self._id},self.json())

    def json(self):
        return {
            "name":self.name,
            "url":self.url,
            "_id":self._id,
            "price":float(self.price)
        }

    @classmethod
    def get_by_id(cls,item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION,{"_id":item_id}))
