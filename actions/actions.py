from context import Context
from intents.intents import Intent


class Action(object):
    def __init__(self, triggering_intent: Intent, ctx: Context):
        self.triggering_intent = triggering_intent
        self.ctx = ctx


class AdditionalSymptomsAction(Action):
    def __init__(self, triggering_intent: Intent, ctx: Context):
        Action.__init__(self, triggering_intent, ctx)


class GreetingAction(Action):
    def __init__(self, ctx: Context):
        Action.__init__(self, None, ctx)


class ShowSymsAction(Action):
    def __init__(self, ctx: Context):
        Action.__init__(self, None, ctx)


class TerminateAction(Action):
    def __init__(self, ctx: Context):
        Action.__init__(self, None, ctx)


class HelpAction(Action):
    def __init__(self, ctx: Context):
        Action.__init__(self, None, ctx)
