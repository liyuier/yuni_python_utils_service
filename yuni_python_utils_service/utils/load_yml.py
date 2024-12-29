import yaml
from ..settings import YML_CONFIG_DIR


def read():
    with open(YML_CONFIG_DIR, 'r', encoding='utf-8') as f:
        data = f.read()
        result = yaml.load(data, Loader=yaml.FullLoader)
    return result
