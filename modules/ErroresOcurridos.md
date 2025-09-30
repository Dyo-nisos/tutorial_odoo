AttributeError: '_unknown' object has no attribute 'id'. Did you mean: 'ids'?
## Ocurrio cuando el modelo estate_property_type no estuvo refereciado en __init__.py


  File "/home/user/odoo/venv-odoo17/lib/python3.13/site-packages/odoo/tools/_monkeypatches.py", line 88, in literal_eval
    return orig_literal_eval(expr)
  File "/usr/lib/python3.13/ast.py", line 64, in literal_eval
    node_or_string = parse(node_or_string.lstrip(" \t"), mode='eval')
  File "/usr/lib/python3.13/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
                   _feature_version=feature_version, optimize=optimize)
  File "<unknown>", line 1
    from . import models
    ^^^^
SyntaxError: invalid syntax

## ocurre cuando no hay un __init__.py en una carpeta

