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

