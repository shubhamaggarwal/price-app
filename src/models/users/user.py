import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.error as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self,email,password,_id=None):
        self.email=email
        self.password=password
        self._id=_id if _id is not None else uuid.uuid4().hex

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email,password):
        """
        user validation done from the database
        :param email: email in the form of a string
        :param password: sha512 hashed password
        :return:
        """
        user_data=Database.find_one('users',{'email':email})
        if user_data is None:
            raise UserErrors.UserNotExists("This user doesn't exist")

        if not Utils.check_hashed_password(password,user_data['password']):
            raise UserErrors.IncorrectPassword("The password you have entered is incorrect!")

        return True

    @classmethod
    def register_user(cls,email,password):
        user_data=Database.find_one('users',{'email':email})

        if user_data is not None:
            raise UserErrors.UserAlreadyExists("This email is already registered with us!")

        if Utils.check_email_is_valid(email):
            new_user = cls(email, Utils.hash_password(password))
            new_user.save_to_db()
            return True
        else:
            raise UserErrors.EmailInvalid("This email is Invalid")



    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION,self.json())

    def json(self):
        return {
            'email':self.email,
            'password':self.password,
            '_id':self._id
        }

    @classmethod
    def get_by_email(cls,email):
        user=cls(**Database.find_one(UserConstants.COLLECTION,{'email':email}))
        return user

    def get_user_alerts(self):
        return Alert.get_alerts_by_email(self.email)
