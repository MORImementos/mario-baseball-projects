import json
from glob import glob
"""display contact and contact type, or result if not contact (needs reconfiguring to accommodate new statfiles I think"""
for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
                stat_file = json.load(json_file)

                for data in stat_file["Events"][:]:
                            pitch = data["Pitch"]

                            contact = pitch.get("Contact", "No contact")

                            if stat_file["Away Player"] == "MORI" and pitch["Pitcher Team Id"] == 1:
                                if pitch.get("Pitch Result") == "Strike-swing" or pitch.get(
                                        "Pitch Result") == "Strike-looking" or pitch.get("Pitch Result") == "Ball":
                                        # contact = pitch.get("Contact", "No contact")
                                        print(contact["Contact Result - Primary"])
                            elif stat_file["Home Player"] == "MORI" and pitch["Pitcher Team Id"] == 0:
                                if pitch.get("Pitch Result") == "Strike-swing" or pitch.get(
                                        "Pitch Result") == "Strike-looking" or pitch.get("Pitch Result") == "Ball":
                                        # contact = pitch.get("Contact", "No contact")
                                        print(contact)
