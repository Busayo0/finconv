import pandas as pd
import xml.etree.ElementTree as ET

def parse_iso8583_xml(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    messages = []
    if root.tag == "isomsg":
        roots = [root]
    else:
        roots = root.findall("isomsg")

    for i, msg in enumerate(roots):
        for field in msg.findall("field"):
            messages.append({
                "Message #": i + 1,
                "Field ID": field.attrib.get("id"),
                "Value": field.attrib.get("value")
            })

    return pd.DataFrame(messages)

def decode_field_48(value):
    return [
        {"Label": "Sample Code", "Value": value[:10]},
        {"Label": "Reference", "Value": value[10:20]},
        {"Label": "Transaction Info", "Value": value[20:30]},
    ]
