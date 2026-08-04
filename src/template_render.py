from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_template(template_name, data):

    template_dir = Path(__file__).resolve().parent.parent / "assets"/ "templates"

    env = Environment(
        loader=FileSystemLoader(template_dir)
    )

    template = env.get_template(template_name)

    return template.render(**data)