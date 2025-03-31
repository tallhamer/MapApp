import json
import requests

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
    "HighResolution": False,
    "PatientSurfaceId": f"{surfaceId}",
    "TreatmentRoomId": f"{treatmentRoomId}",
    "Isocenter": {
        "x": "38.8129272460938",
        "y": "-142.63232421875",
        "z": "153.504974365234",
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
        "x": "38.8129272460938",
        "y": "-142.63232421875",
        "z": "153.504974365234",
        "CoordinateSystem": "IEC_61217"
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
        },
        {
            "beamNumber": 2,
            "controlPoints": [
                {
                    "gantryAngle": 1,
                    "couchAngle": 0,
                    "coordinateSystem": "Native"
                },
                {
                    "gantryAngle": 2,
                    "couchAngle": 0,
                    "coordinateSystem": "Native"
                },
                {
                    "gantryAngle": 3,
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

response = requests.get(get_url, headers=headers, verify=False)
# response = requests.post(put_url, json=beamDeliveryStatusBody, headers=headers, verify=False)

if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)