import json
from icecream import ic


def read_from_json(file):
    try:
        with open(file, encoding="utf-8") as f:
            result = json.load(f)
        return result
    except Exception as e:
        ic("read file error: " + file)
        ic(e)
        return None

