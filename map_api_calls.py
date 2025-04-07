import glob
import numpy as np

import json
import requests



# data = {}
# for path in glob.glob(r"C:\__python__\Projects\MapApp\data\MapRT_Exports\*"):
#     data[path] = {}
#     with open(path, 'r') as f:
#         for point in f:
#             if len(point.split(';')) == 3:
#                 d = {}
#                 gantry, couch, collision = point.split(';')
#                 c = False if collision.strip() == '0' else True
#
#                 if gantry.strip not in data[path]:
#                     d[couch.strip()] = c
#                     data[path][gantry.strip()] = d
#                 else:
#                     if couch.strip() not in data[path][gantry.strip()]:
#                         data[path][gantry.strip()][couch.strip()] = c
#                     else:
#                         print(f"Duplicate entry found for G: {gantry.strip()} C: {couch.strip()}")
#             else:
#                 print(point)

api_url = "https://maprtpkr.adventhealth.com:5000"
token = "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
user_agent = "VisionRT.Integration.Saturn/1.2.8"
patientId = "PHY0019"
treatmentRoomId = "eaf6df9d-8e60-c46a-4e6f-ca55e7470545"
machineName = "Truebeam"
surfaceId = "2e36321f-19de-49cd-899d-c772da051316"

# Endpoints
grtStatus = f"/integration/ping"
getAllTxRooms = f"/integration/rooms"
getSingleTxRoom = f"/integration/rooms/{machineName}"
getSurfaceForPatient = f"/integration/patients/{patientId}/surfaces"
getSurface = f"/integration/surfaces/{surfaceId}"
getMap = f"/integration/GetMap"
getBeamDeliveryStatus = f"/integration/GetBeamDeliveryStatus"

# Body
empty = ""
mapBody = \
    {
    "CouchBuffer": 20,
    "PatientBuffer": 20,
    "HighResolution": True,
    "PatientSurfaceId": f"{surfaceId}",
    "TreatmentRoomId": f"{treatmentRoomId}",
    "Isocenter": {
        "x": 141.3,
        "y": 74.9,
        "z": 670.3,
        "CoordinateSystem": "IEC_61217",
        }
    }

beamDeliveryStatusBody = \
{
    "CouchBuffer": 20,
    "PatientBuffer": 20,
    "PatientSurfaceId": f"{surfaceId}",
    "TreatmentRoomId": f"{treatmentRoomId}",
    "Isocenter": {
        "x": 141.3,
        "y": 74.9,
        "z": 670.3,
        "CoordinateSystem": "IEC_61217",
    },
    "BeamList":[
        {
            "beamNumber": 1,
            "controlPoints": [
                {
                    "gantryAngle": 0,
                    "couchAngle": 0,
                    "coordinateSystem": "Native"
                }
            ]
        }
    ]
}

print(json.dumps(mapBody))

get_url = api_url + getAllTxRooms
put_url = api_url + getBeamDeliveryStatus

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": user_agent
}

# response = requests.get(get_url, headers=headers, verify=False)
response = requests.post(put_url, json=beamDeliveryStatusBody, headers=headers, verify=False)

if response.status_code == 200:
    print("Request successful!")
    print(response.json())
    # print(response.text.split())
    # test_data = {}
    # for i, p in enumerate(response.text.split()):
    #     if len(p.split(',')) == 3:
    #         d = {}
    #         couch, gantry, collision = p.split(',')
    #         c = False if collision.strip() == '0' else True
    #
    #         test_data[gantry.strip()] = d
    #
    #         if gantry.strip not in test_data:
    #             d[couch.strip()] = c
    #             test_data[gantry.strip()] = d
    #         else:
    #             if couch.strip() not in test_data[gantry.strip()]:
    #                 test_data[gantry.strip()][couch.strip()] = c
    #             else:
    #                 print(f"Duplicate entry found for G: {gantry.strip()} C: {couch.strip()} in test_data")
    #
    #     else:
    #         print(p)
    #
    # for path in data:
    #     for g in test_data:
    #         if g not in data[path]:
    #             print(f'G{g} not in reference data source {path}')
    #         else:
    #             for c in test_data[g]:
    #                 if c not in data[path][g]:
    #                     print(f'G{g}, C{c} not in reference data source {path}')
    #                 else:
    #                     if data[path][g][c] and not test_data[g][c]:
    #                         print(f"Found difference at G{g} C{c} - Data: {data[path][g][c]} - Test_Data: {not test_data[g][c]} in {path}")
    #
    # print(data)
    # print(test_data)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)