from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def format_number(value):

    if value is None:
        return ""

    value = round(float(value))

    s = str(int(value))

    if len(s) <= 3:
        return s

    last_three = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return ",".join(parts + [last_three])

def render_template(template_name, data):

    template_dir = Path(__file__).resolve().parent.parent / "assets"/ "templates"

    env = Environment(
        loader=FileSystemLoader(template_dir)
    )

    env.filters["format_number"] = format_number

    template = env.get_template(template_name)

    return template.render(**data)