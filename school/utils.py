import random
import string

def fourRandomDigits():
    fourdigits = random.randint(1111,9999)
    return fourdigits

def alphaNumericLock():
    s = ''
    d = string.ascii_letters + '1234567890-'
    try:
        for i in range(11):
            f = d[random.randint(0, len(d))]
            s += f
        return s
    except:
        return alphaNumericLock()


def unread_messages(self,request):
    count = 0
    notification = self.request.user.student.notification_set.all()
    for messages in notification:
        if not self.request.user.student in messages.read.all():
            count = count + 1
    return count 