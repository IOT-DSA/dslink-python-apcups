import dslink
import subprocess32
from twisted.internet.task import LoopingCall


def get_key_values():
    process = subprocess32.Popen(["apcaccess"], stdout=subprocess32.PIPE)
    key_values = []
    for i in process.stdout.read().split("\n"):
        j = i.split(":", 1)
        if len(j) > 1:
            key_values.append([j[0].strip(), j[1].strip()])
    return key_values

known_types = {
    "LINEV": "number",
    "LOADPCT": "number",
    "BCHARGE": "number",
    "TIMELEFT": "number",
    "MBATTCHG": "number",
    "MINTIMEL": "number",
    "MAXTIME": "number",
    "OUTPUTV": "number",
    "DWAKE": "number",
    "LOTRANS": "number",
    "HITRANS": "number",
    "ALARMDEL": "number",
    "NUMXFERS": "number",
    "TONBATT": "number",
    "CUMONBATT": "number",
    "NOMINV": "number",
    "NOMPOWER": "number"
}


def parse(data, key):
    i = data.split(" ")
    if key not in known_types:
        i[0] = data
    print(key)
    if key in known_types:
        if known_types[key] == "number":
            i[0] = float(i[0])
    return i


class APCDSLink(dslink.DSLink):
    def start(self):
        poll_loop = LoopingCall(self.update)
        poll_loop.start(1)

    def get_default_nodes(self, super_root):
        key_values = get_key_values()

        for pair in key_values:
            node = super_root.create_child(pair[0])
            if pair[0] in known_types:
                node.set_type(known_types[pair[0]])
                parsed = parse(pair[1], pair[0])
                node.set_value(parsed[0])
                if len(parsed) > 1:
                    node.set_attribute("@unit", parsed[1])
            else:
                node.set_type("dynamic")
                node.set_value(pair[1])

        return super_root

    def update(self):
        super_root = self.responder.super_root
        key_values = get_key_values()

        for pair in key_values:
            if super_root.has_child(pair[0]):
                node = super_root.get("/" + pair[0])
                parsed = parse(pair[1], pair[0])
                node.set_value(parsed[0])
                if len(parsed) > 1:
                    node.set_attribute("@unit", parsed[1])
            else:
                node = super_root.create_child(pair[0])
                if pair[0] in known_types:
                    node.set_type(known_types[pair[0]])
                    parsed = parse(pair[1], pair[0])
                    node.set_value(parsed[0])
                    if len(parsed) > 1:
                        node.set_attribute("@unit", parsed[1])
                else:
                    node.set_type("dynamic")
                    node.set_value(pair[1])


if __name__ == "__main__":
    APCDSLink(dslink.Configuration("APCUPS", True, no_save_nodes=True))
