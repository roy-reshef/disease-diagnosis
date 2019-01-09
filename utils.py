from typing import List

from context import Context


def get_user_syms(user_input: str, ctx: Context) -> List[str]:
    user_syms = []
    doc = ctx.nlp(user_input)
    matches = ctx.sym_matcher(doc)

    for match_id, start, end in matches:
        rule_id = ctx.nlp.vocab.strings[match_id]
        span = doc[start: end]
        user_syms.append(span.text)

    return user_syms

def end_session(ctx: Context):
    if len(ctx.possible_diseases) > 0:
        print('\nhealth condition diagnosis finished')
        print("possible condition(s) you might suffer from:", ",".join(ctx.possible_diseases))
    else:
        print("possible health condition is not diagnosed. sorry.")

    print("bye for now. i am glad to be of help")
