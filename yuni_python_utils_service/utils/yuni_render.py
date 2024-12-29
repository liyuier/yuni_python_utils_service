from jinja2 import Template, FileSystemLoader, Environment

from yuni_python_utils_service.settings import TEMPLATE_DIR


def get_template(template_name: str) -> Template:
    file_loader = FileSystemLoader(str(TEMPLATE_DIR))
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    return template
