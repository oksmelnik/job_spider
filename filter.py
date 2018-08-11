import json
import re

with open('tmp/jobs.json') as json_data:
    d = json.load(json_data)

list = []
for x in d:
        y = re.sub("\D", "", x['posted'])
        try:
            if int(y) < 7:
                list.append(x['link'])
        except ValueError:
            pass

with open("res.json", 'w') as f:
    json.dump(list, f)
