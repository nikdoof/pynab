

class InvalidBudget(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __unicode__(self):
        return self.msg