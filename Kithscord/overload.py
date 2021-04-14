user_cmds = {}
admin_cmds = {}

_export_arg = 0
_export_admin = False


def export(arg: int, is_admin_cmd=False):
    global _export_arg, _export_admin

    _export_arg = arg
    _export_admin = is_admin_cmd

    return _export


def _export(func):
    cmds = admin_cmds if _export_admin else user_cmds

    if func.__name__ not in cmds.keys():
        cmds[func.__name__] = {}
    cmds[func.__name__][_export_arg] = func

    return func
