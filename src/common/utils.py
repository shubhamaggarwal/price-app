from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        :param password: sha512 password from the form
        :return: sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password,hashed_password):
        """
        :param password:sha512 password received in form
        :param hashed_password:password stored in database pbkdf2 encryption
        :return:
        """
        return pbkdf2_sha512.verify(password,hashed_password)

    @staticmethod
    def check_email_is_valid(email):
        email_matcher=re.compile('^[\w]+@([\w]+\.)+[\w]+$')
        return True if email_matcher.match(email) else False