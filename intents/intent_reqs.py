import json

from context import Context


class IntentReq(object):

    def __init__(self, ctx: Context):
        self.ctx = ctx


class UserInputIntentReq(IntentReq):

    def __init__(self, ctx: Context):
        IntentReq.__init__(self, ctx)

    def __repr__(self):
        return {
            'intent request': 'user input request'
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)


class TerminateIntentReq(IntentReq):

    def __init__(self, ctx: Context):
        IntentReq.__init__(self, ctx)

    def __repr__(self):
        return {
            'intent request': 'terminate request'
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
