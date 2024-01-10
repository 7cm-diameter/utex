from typing import Optional


def namefile(
    meta: dict,
    timeformat: Optional[str] = "%y%m%d%H%M",
    tfseparator: Optional[str] = "-",
    separator: str = "_",
    extension: str = "csv",
) -> str:
    """docstring for namefile"""
    from datetime import datetime

    now = ""
    if timeformat is not None:
        if tfseparator is not None:
            components = list(filter(lambda c: c != "", timeformat.split("%")))
            timeformat = "%" + (tfseparator + "%").join(components)
        now = datetime.now().strftime(timeformat)
    experiment = meta.get("experiment", "")
    sub = meta.get("subject", "")
    cond = meta.get("condition", "")
    components = [experiment, sub, cond, now]
    try:
        components = list(filter(lambda c: c != "", components))
    except ValueError:
        pass
    stem = separator.join(components)
    if extension.startswith("."):
        return stem + extension
    return stem + "." + extension


def get_current_file_abspath(relpath: str) -> str:
    from os.path import abspath, dirname

    return dirname(abspath(relpath))
