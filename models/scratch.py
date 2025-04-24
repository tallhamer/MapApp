import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.sequence import Sequence

# File meta info data elements
file_meta = FileMetaDataset()
file_meta.FileMetaInformationGroupLength = 192
file_meta.FileMetaInformationVersion = b'\x00\x01'
file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
file_meta.MediaStorageSOPInstanceUID = '1.2.246.352.62.1.4617159606128845690.1628241455863929788'
file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
file_meta.ImplementationClassUID = '1.2.246.352.70.2.1.163.2'
file_meta.ImplementationVersionName = 'File Svc 16.1'

# Main data elements
ds = Dataset()
ds.SpecificCharacterSet = 'ISO_IR 192'
ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL']
ds.InstanceCreationDate = '20250423'
ds.InstanceCreationTime = '081030'
ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
ds.SOPInstanceUID = '1.2.246.352.62.1.4617159606128845690.1628241455863929788'
ds.StudyDate = '20220614'
ds.SeriesDate = '20220707'
ds.AcquisitionDate = '20220707'
ds.ContentDate = '20220707'
ds.StudyTime = '081756.95'
ds.SeriesTime = '140954.797'
ds.AcquisitionTime = '140835.823'
ds.ContentTime = '140835.823'
ds.AccessionNumber = ''
ds.Modality = 'CT'
ds.Manufacturer = 'Varian Medical Systems'
ds.ReferringPhysicianName = ''
ds.StationName = 'TrueBeam2422'
ds.StudyDescription = 'SBRT Brain'
ds.PhysiciansOfRecord = 'Bugoci^Darlene'
ds.OperatorsName = 'DICOM Service'
ds.ManufacturerModelName = 'Patient Verification'

# Referenced Instance Sequence
refd_instance_sequence = Sequence()
ds.ReferencedInstanceSequence = refd_instance_sequence

# Referenced Instance Sequence: Referenced Instance 1
refd_instance1 = Dataset()
refd_instance_sequence.append(refd_instance1)
refd_instance1.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.5'
refd_instance1.ReferencedSOPInstanceUID = '1.2.246.352.71.5.518672833859.394172.20220615094941'

# Purpose of Reference Code Sequence
purpose_of_ref_code_sequence = Sequence()
refd_instance1.PurposeOfReferenceCodeSequence = purpose_of_ref_code_sequence

# Purpose of Reference Code Sequence: Purpose of Reference Code 1
purpose_of_ref_code1 = Dataset()
purpose_of_ref_code_sequence.append(purpose_of_ref_code1)
purpose_of_ref_code1.CodeValue = '1000'
purpose_of_ref_code1.CodingSchemeDesignator = '99VMS_PURPREFOBJ'
purpose_of_ref_code1.CodingSchemeVersion = '1.0'
purpose_of_ref_code1.CodeMeaning = 'RT Plan or RT Ion Plan or Radiation Set to be verified'

ds.IrradiationEventUID = '1.2.246.352.62.30.5408731356369236876.1481870726010384521'
ds.PatientName = 'Swaney^Tarah'
ds.PatientID = 'CEUE02352266'
ds.PatientBirthDate = '19841205'
ds.PatientBirthTime = '000000'
ds.PatientSex = 'F'
ds.ScanOptions = 'STANDARD'
ds.SliceThickness = '0.9948622684036'
ds.KVP = '100.0'
ds.DataCollectionDiameter = '261.72965811982'
ds.DeviceSerialNumber = '2422'
ds.SoftwareVersions = '2.24.0.0'
ds.ReconstructionDiameter = '261.72965811982'
ds.DistanceSourceToDetector = '1500.0'
ds.DistanceSourceToPatient = '1000.0'
ds.GantryDetectorTilt = '0.0'
ds.TableHeight = '132.83267115081'
ds.RotationDirection = 'CC'
ds.ExposureTime = '17900'
ds.XRayTubeCurrent = '40'
ds.Exposure = '716'
ds.FilterType = 'Tit V1,FF V1'
ds.FocalSpots = '1.0'
ds.ConvolutionKernel = 'Ram-Lak'
ds.PatientPosition = 'HFS'
ds.CTDIvol = 15.107599999999998

# CTDI Phantom Type Code Sequence
ctdi_phantom_type_code_sequence = Sequence()
ds.CTDIPhantomTypeCodeSequence = ctdi_phantom_type_code_sequence

# CTDI Phantom Type Code Sequence: CTDI Phantom Type Code 1
ctdi_phantom_type_code1 = Dataset()
ctdi_phantom_type_code_sequence.append(ctdi_phantom_type_code1)
ctdi_phantom_type_code1.CodeValue = '113690'
ctdi_phantom_type_code1.CodingSchemeDesignator = 'DCM'
ctdi_phantom_type_code1.CodingSchemeVersion = '20061023'
ctdi_phantom_type_code1.CodeMeaning = 'IEC Head Dosimetry Phantom'

ds.StudyInstanceUID = '1.3.46.670589.33.1.63790791470103767100001.4999043011036486573'
ds.SeriesInstanceUID = '1.2.246.352.62.2.4706266107867560264.28727925019077043'
ds.StudyID = '3668'
ds.SeriesNumber = '7'
ds.AcquisitionNumber = '1'
ds.InstanceNumber = '166'
ds.ImagePositionPatient = [-132.20240390788, -130.66080279022, 69.0666432352228]
ds.ImageOrientationPatient = [0.99994191676809, -0.0089995973578, 0.0059304584616, 0.0088951357783, 0.99980884071293, 0.01741145001856]
ds.FrameOfReferenceUID = '1.2.246.352.62.3.5025055500600017485.16126252829569318273'
ds.PositionReferenceIndicator = ''
ds.ImageComments = 'Reconstruction Mode THREE_D\r\nFilter AUTO\r\nRing Suppression MEDIUM\r\n'
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = 'MONOCHROME2'
ds.Rows = 512
ds.Columns = 512
ds.PixelSpacing = [0.51119073851527, 0.51119073851527]
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 0
ds.WindowCenter = '37.0'
ds.WindowWidth = '468.0'
ds.RescaleIntercept = '-1000.0'
ds.RescaleSlope = '1.0'
ds.RescaleType = 'HU'
ds.PatientSupportAngle = '359.66015625'
ds.TableTopLongitudinalPosition = '404.540597694848'
ds.TableTopLateralPosition = '-19.194035945886'
ds.TableTopPitchAngle = 359.0023498535156
ds.TableTopRollAngle = 0.5097377300262451
ds.PixelData = # XXX Array of 524288 bytes excluded

ds.file_meta = file_meta
ds.is_implicit_VR = True
ds.is_little_endian = True
ds.save_as(r'.\CT.1.2.246.352.62.1.4617159606128845690.1628241455863929788_from_codify.dcm', write_like_original=False)
