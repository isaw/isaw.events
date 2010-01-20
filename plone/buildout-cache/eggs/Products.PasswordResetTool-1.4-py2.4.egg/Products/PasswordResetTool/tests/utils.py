from Products.SecureMailHost.SecureMailHost import SecureMailHost as MailBase


class MockMailHost(MailBase):
    """A MailHost that collects messages instead of sending them.

    Thanks to Rocky Burt for inspiration.
    """

    def __init__(self, id):
        MailBase.__init__(self, id, smtp_notls=True)
        self.reset()

    def reset(self):
        self.messages = []

    def send(self, message, mto=None, mfrom=None, subject=None, encode=None):
        """
        Basically construct an email.Message from the given params to make sure
        everything is ok and store the results in the messages instance var.
        """
        self.messages.append(message)

    def secureSend(self, message, mto, mfrom, **kwargs):
        kwargs['debug'] = True
        result = MailBase.secureSend(self, message=message, mto=mto,
                                     mfrom=mfrom, **kwargs)
        self.messages.append(result)

    def validateSingleEmailAddress(self, address):
        return True # why not
