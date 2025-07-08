import os
import json
import base64
from typing import Optional
from pydantic import BaseModel, Base64Str


class DicomSettings(BaseModel):
    dicom_data_directory: str = '.'
    arc_check_resolution: int = 1
    surface_recon_method: str = 'Zero-Crossing'
    pixel_spacing_x: float = 1.0
    pixel_spacing_y: float = 1.0
    contours_to_keep: str = 'ALL'

class MapRTSettings(BaseModel):
    api_url: str = "https://localhost:5000"
    api_token: Optional[Base64Str] = None
    api_user_agent: str = "VisionRT.Integration.Saturn/1.2.8"


class AppSettings(BaseModel):
    dicom: DicomSettings
    maprt: MapRTSettings

base_settings = b'ew0KICAgICJkaWNvbSI6IHsNCiAgICAgICAgImRpY29tX2RhdGFfZGlyZWN0b3J5IjogIkM6L3RtcC9tYXAgYXBwIGRhdGEiLA0KICAgICAgICAiYXJjX2NoZWNrX3Jlc29sdXRpb24iOiAxLA0KICAgICAgICAic3VyZmFjZV9yZWNvbl9tZXRob2QiOiAiWmVyby1Dcm9zc2luZyIsDQogICAgICAgICJwaXhlbF9zcGFjaW5nX3giOiAxLjAsDQogICAgICAgICJwaXhlbF9zcGFjaW5nX3kiOiAxLjAsDQogICAgICAgICJjb250b3Vyc190b19rZWVwIjogIkNDVyINCiAgICB9LA0KICAgICJtYXBydCI6IHsNCiAgICAgICAgImFwaV91cmwiOiAiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwMCIsDQogICAgICAgICJhcGlfdG9rZW4iOiAiVGxSck1scHFZekZPZWtsNVRVUlZNRTV0V1RKWmFsa3hUbTFWZVUxRVVUUk9hbFV6VFdwWk1RPT0iLA0KICAgICAgICAiYXBpX3VzZXJfYWdlbnQiOiAiVmlzaW9uUlQuSW50ZWdyYXRpb24uU2F0dXJuLzEuMi44Ig0KICAgIH0NCn0='
if not os.path.exists(r'./settings.json'):
    with open(r'./settings.json', 'wb') as w:
        w.write(base64.b64decode(base_settings))

settings_file = open(r'./settings.json', 'r')
settings_data = json.load(settings_file)
app_settings = AppSettings(**settings_data)