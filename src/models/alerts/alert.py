import uuid
import requests
import src.models.alerts.constants as AlertConstants
import datetime
from src.common.database import Database
from src.models.items.item import Item

class Alert(object):
    def __init__(self,user_email,item_id,price_limit,active=True,time_last_checked=None,_id=None):
        self.user_email=user_email
        self.item=Item.get_by_id(item_id)
        self.price_limit=float(price_limit)
        self.time_last_checked=datetime.datetime.utcnow() if time_last_checked is None else time_last_checked
        self._id=uuid.uuid4().hex if _id is None else _id
        self.active=active

    def __repr__(self):
        return "<Alert for {} for {} with limit = {}>".format(self.user_email, self.item.name, self.price_limit)

    def send_alert_message(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                  "from": AlertConstants.FROM,
                  "to": [self.user_email],
                  "subject": "{} has reached the price limit!".format(self.item.name),
                  "text": "You can straight away head to the store by clicking this link {} .!".format(self.item.url)
                  }
        )

    @classmethod
    def find_need_update(cls,time_limit=AlertConstants.TIME_BEFORE_CHECK):
        last_updated_limit=datetime.datetime.utcnow()-datetime.timedelta(minutes=time_limit)

        return [cls(**elem) for elem in Database.find_all(AlertConstants.COLLECTION,
                                                          query={"time_last_checked":{"$lte":last_updated_limit},"active":False}
                                                          )
                ]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION,{'_id':self._id},self.json())

    def json(self):
        return {
            "_id":self._id,
            "user_email":self.user_email,
            "price_limit":self.price_limit,
            "time_last_checked":self.time_last_checked,
            "item_id":self.item._id,
            "active":self.active
        }

    def load_item_price(self):
        self.time_last_checked=datetime.datetime.utcnow()
        self.item.price=self.item.load_price()
        self.update_in_mongo()
        self.item.save_to_mongo()
        return self.item.price

    def send_if_price_reached(self):
        if float(self.price_limit)>=float(self.item.price):
            self.send_alert_message()

    def update_in_mongo(self):
        Database.update(AlertConstants.COLLECTION,{'_id':self._id},self.json())

    @classmethod
    def get_alerts_by_email(cls,email):
        print(email)
        return [cls(**elem) for elem in Database.find_all(AlertConstants.COLLECTION,{'user_email':email})]

    @classmethod
    def get_by_id(cls,alert_id):
        print(alert_id)
        return cls(**Database.find_one(AlertConstants.COLLECTION,{'_id':alert_id}))

    @staticmethod
    def convert_data_for_alert_to_item(name,url):
        item = Item(name=name,url=url)
        item.load_price()
        item.save_to_mongo()
        return item

    def activate(self):
        self.active=True
        self.update_in_mongo()

    def deactivate(self):
        self.active=False
        self.update_in_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION,{'_id':self._id})
