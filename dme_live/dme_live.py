import code

# you don't need rich, but I like it because it makes the terminal look a lot more pleasant
# import rich
from rich import pretty

import memory_engine as me


dme_functions = {}
rich_functions = {}
for name in dir(me):
    obj = getattr(me, name)
    if callable(obj):
        dme_functions[name] = obj
# for name in dir(rich):
#     obj = getattr(rich, name)
#     if callable(obj):
#         rich_functions[name] = obj

locals().update(dme_functions)
# locals().update(rich_functions)

pretty.install()
"""TYPE 'dme_functions' IN TERMINAL WINDOW TO GET LIST OF AVAILABLE FUNCTIONS"""

"""Type 'locals()' or 'dir()' to get a list of available functions and active variables. """
code.interact(local=locals())
