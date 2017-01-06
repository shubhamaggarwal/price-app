import os
URL = os.environ.get(MAILGUN_URL)
FROM=os.environ.get(MAILGUN_FROM)
API_KEY=os.environ.get(MAILGUN_API_KEY)
TIME_BEFORE_CHECK = 10
COLLECTION = 'alerts'
