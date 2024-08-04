# from icecream import ic
import os
import json

# ic(os.environ)
with open("ss.json", "w+") as f:
    d = {}
    for k, v in os.environ.items():
        d[k] = v
    json.dump(d, f)
