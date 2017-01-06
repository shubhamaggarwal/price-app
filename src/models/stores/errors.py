class StoreError(Exception):
    def __int__(self,message):
        self.message=message


class StoreNotFound(StoreError):
    pass