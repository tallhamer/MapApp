import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# construct couch index map
c0 = np.arange(270,360,1)
# print(c0)
i0 = np.arange(len(c0))
# print(i0)

c1 = np.arange(0,91,1)
couch = np.hstack((c0, c1))
# print(couch)
i1 = np.arange(len(c1)) + len(c0)
i = np.hstack((i0, i1))
# print(i)

g0 = np.arange(181,360,1)
# print(g0)
j0 = np.arange(len(g0))
# print(j0)

g1 = np.arange(0,181,1)
gantry = np.hstack((g0, g1))
# print(gantry)
j1 = np.arange(len(g1)) + len(g0)
j = np.hstack((j0, j1))
# print(j)

x_map = dict([(str(couch[x]), int(i[x])) for x in range(len(i))])
y_map = dict([(str(gantry[y]), int(j[y])) for y in range(len(j))])
print(x_map)
print(y_map)

api_image = np.zeros((len(j), len(i)))
export_image = np.zeros((len(j), len(i)))
bs_image = np.zeros((len(j), len(i)))

api_url = "https://maprtpkr.adventhealth.com:5000"
token = "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
user_agent = "VisionRT.Integration.Saturn/1.2.8"
patientId = "PHY0019"
treatmentRoomId = "eaf6df9d-8e60-c46a-4e6f-ca55e7470545"
machineName = "Truebeam"
surfaceId = "3ec6afa2-9130-4123-a862-0a91db937a95" #"2e36321f-19de-49cd-899d-c772da051316"

# Endpoints
grtStatus = f"/integration/ping"
getAllTxRooms = f"/integration/rooms"
getSingleTxRoom = f"/integration/rooms/{machineName}"
getSurfaceForPatient = f"/integration/patients/{patientId}/surfaces"
getSurface = f"/integration/surfaces/{surfaceId}"
getMap = f"/integration/GetMap"
getBeamDeliveryStatus = f"/integration/GetBeamDeliveryStatus"

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": user_agent
}

# Body
mapBody = \
    {
    "CouchBuffer": 20,
    "PatientBuffer": 20,
    "HighResolution": True,
    "PatientSurfaceId": f"{surfaceId}",
    "TreatmentRoomId": f"{treatmentRoomId}",
    "Isocenter": {
        "x": 17.3, #141.3,
        "y": 69.4, #74.9,
        "z": 218.7, #670.3,
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
                "BeamList": [
                ]
            }

count = 0
res_map = {}
for couch_val in couch:
    for gantry_val in gantry:
        count+=1
        beam = {
            "beamNumber": count,
            "controlPoints": [
                {
                    "gantryAngle": int(gantry_val),
                    "couchAngle": int(couch_val),
                    "coordinateSystem": "Native"
                }
            ]
        }
        res_map[count] = {'gantry':str(gantry_val), 'couch':str(couch_val)}
        beamDeliveryStatusBody["BeamList"].append(beam)
print(beamDeliveryStatusBody)

put_url = api_url + getBeamDeliveryStatus
response = requests.post(put_url, json=beamDeliveryStatusBody, headers=headers, verify=False)
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
    data = response.json()
    for status in data['data']['statuses']:
        g = res_map[status["beamNumber"]]['gantry']
        c = res_map[status["beamNumber"]]['couch']
        isSafe = status['isSafe']

        val = 1 if isSafe else 0
        print('>>', g, c, isSafe)
        print(y_map[g], x_map[c], val)

        bs_image[y_map[g], x_map[c]] = val
        print(bs_image[y_map[g], x_map[c]])
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)

print(bs_image)


put_url = api_url + getMap
response = requests.post(put_url, json=mapBody, headers=headers, verify=False)
if response.status_code == 200:
    print("Request successful!")
    for i, p in enumerate(response.text.split()):
        if len(p.split(',')) == 3:
            couch, gantry, collision = p.split(',')
            c = 0 if collision.strip() == '0' else 1

            api_image[y_map[gantry], x_map[couch]] = c
        else:
            print(p)



export_path = r"C:\__python__\Projects\MapApp\data\MapRT_Exports\507261791 For MapRT 20250404134828.csv"
with open(export_path, 'r') as f:
    for line in f:
        if not line.startswith('Gantry'):
            if len(line.split(';')) == 3:
                gantry, couch, collision = line.split(';')
                c = 1 if collision.strip() == 'false' else 0

                export_image[y_map[gantry], x_map[couch]] = c

            else:
                print(line)


# Create the plot
fig, axes = plt.subplots(1,3)

ex_plot = axes[0].imshow(export_image, cmap='jet', extent=[0, 180, 0, 180])
api_plot = axes[1].imshow(api_image, cmap='jet', extent=[0, 180, 0, 180])
bs_plot = axes[1].imshow(bs_image, cmap='jet', extent=[0, 180, 0, 180])
# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()