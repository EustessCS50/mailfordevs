from . models import Mail

def count_mails(user:object):
    no_mails = Mail.objects.filter(dev=user).count()
    return no_mails
