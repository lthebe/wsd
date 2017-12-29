from hashlib import md5
from django.conf import settings
# get md5 digest to send to the payment request
def get_checksum( amount, pid, sid=settings.SELLER_ID, secret_key=settings.PAYMENT_KEY):
    message = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    return md5(message.encode("ascii")).hexdigest()
