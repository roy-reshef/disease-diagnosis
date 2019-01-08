import json

from context import Context
from intents.intent_reqs import IntentReq


class Intent(object):

    def __init__(self, ctx: Context, intent_req: IntentReq = None):
        self.ctx = ctx
        self.intent_req = intent_req


class UserInputIntent(Intent):

    def __init__(self, ctx: Context, user_input: str):
        Intent.__init__(self, ctx)
        self.user_input = user_input

    def __repr__(self):
        return {
            'intent': 'user input',
            'user input': self.user_input
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)


class NoIntent(Intent):

    def __init__(self, ctx: Context):
        Intent.__init__(self, ctx)

    def __repr__(self):
        return {
            'intent': 'no intent',
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)
