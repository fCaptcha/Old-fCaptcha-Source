import json
from hashlib import md5

import flask

from hcap_solver import database_fps, HSW

flask2 = flask.Flask(__name__)
reference_fingerprint = json.load(open("n.json", "r"))
events = []
for reference_event in reference_fingerprint["events"]:
    events.append(reference_event[0])


@flask2.post("/grab-hsw")
def pull():
    data = json.loads(HSW.decrypt(flask.request.data.decode()))
    event_ids = []
    for event in data["events"]:
        if event[0] not in events or isinstance(json.loads(event[1]), int):
            event_ids.append(event[0])
            data["events"].remove(event)
    data = json.dumps(data)
    md5_hash = md5(data.encode()).hexdigest().upper()
    print(f"Got Fingerprint: {md5_hash} | Popped Events: {event_ids}")
    database_fps.set(md5_hash, data)
    return f"OK|{md5_hash}"


if __name__ == '__main__':
    flask2.run("0.0.0.0", 6969, debug=True)
