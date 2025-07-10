<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tallhamer/MapApp.git">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MapApp</h3>

  <p align="center">
    An example project to illustrate some of the <a href="https://visionrt.com/our-solutions/maprt-api/">MapRT API</a> integration possibilities. The application is a standalone 
    python application that connects to the MapRT API and provides DICOM plan validation and clearance map visualization.
    <br /> 
    <br />
    While the application seeks to simply show integration strategies with MapRT's API it also provides some clinical 
    features that users may find useful in their clinical practice. The application is provided under the MIT license and 
    can be used in clinical practice at the user's own risk.  
    <br />
    <a href="#getting-started"><strong>Explore the docs »</strong></a>
    <br />
    <br /><br />
    <!--
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    -->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#creating-a-binary-application">Creating a Binary Application</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
        <ul>
        <li><a href="#initial-setup">Initial Setup</a>
          <ul>
            <li><a href="#dICOM-settings">DICOM Settings</a></li>
            <li><a href="#mapRT-settings">MapRT Settings</a></li>
          </ul>
        </li>
        <li><a href="#opening-dICOM-files">Opening DICOM Files</a>
          <ul>
            <li><a href="#3D-view-manipulation-and-mouse-controls">3D View Manipulation and Mouse Controls</a></li>
            <li><a href="#visual-settings">Visual Settings</a></li>
          </ul>
        </li>
        <li><a href="#connection-to-the-mapRT-aPI">Connection to the MapRT API</a>
          <ul>
            <li><a href="#surface-alignment-checks">Surface Alignment Checks</a></li>
            <li><a href="#virtual-simulations">Virtual Simulations</a></li>
            <li><a href="#experimental-synthetic-cTs">Experimental Synthetic CTs</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Project Screen Shot][project-screenshot]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python 3.12.9](https://img.shields.io/badge/Python-3.12.9-blue?logo=python&logoColor=white)](https://www.python.org)
[![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-41cd52?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![VTK](https://img.shields.io/badge/VTK-Visualization%20Toolkit-ff6600?style=flat)](https://vtk.org)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
1. If you don't already have it installed, install [Python](https://www.python.org/downloads/). I recommend version 3.12 but any version 3.10 or above should work 
    

2. Navigate to a root folder where you would like to store the virtual environment. Create a virtual python environment
   by executing the following command. (Replace *myenv* with the name of your virtual environment)
    ```sh
      python -m venv myenv
    ```
3. Navigate to the *Scripts* folder under the new *myenv* folder and activate the virtual environment using the proper 
activate script.
   ### Windows (Command prompt):
    ```sh
      myenv\Scripts\activate.bat
    ```
   ### On Windows (PowerShell):
    ```sh
      myenv\Scripts\Activate.ps1
    ```
   ### On macOS/Linux:
    ```sh
      source myenv/bin/activate
    ```
   
4. If you have [Git](https://git-scm.com/) installed, clone the github repo for this project using the command below or 
simply download the code from the [repo](https://github.com/tallhamer/MapApp) and unzip the resulting archive to a 
location on your hard drive.
    ```sh
      git clone https://github.com/tallhamer/MapApp.git
    ```
5. With the virtual python environment activated, navigate to the location of the cloned git repo and install the 
project dependencies using the *requirement.txt* file.
    ```sh
      pip install -r requirements.txt
    ```
After all dependencies have been successfully installed, you should be able to type the following command at the command 
prompt of the activated virtual python environment to launch the application.
```sh
   python map_app.py
```

### Creating a Binary Application
If you don't want to have to activate the virtual python environment each time you want to run the application you can 
generate a standalone executable (.exe) file on windows.

1. Activating the virtual python environment using the steps above.

2. Navigate to the location where you cloned the MapApp repo

3. Verify that the *map_app.spec* file is located in the root directory

4. Run the following command
    ```sh
      pyinstaller map_app.spec
    ```
5. If you are missing the *map_app.spec* file you can run the following command replacing *FullPathToRepoFolder* with the 
   path to the cloned repository on your machine.
    ```sh
      pyinstaller map_app.py --paths=FullPathToRepoFolder -D --hidden-import=vtkmodules.util.data_model --hidden-import=vtkmodules.util.execution_model --hidden-import=skimage._shared.geometry 
    ```
The result should be a *dist* folder with a subfolder named *map_app*. You can move the *map_app* folder to any location 
and run the *map_app.exe* inside the folder to use the application without needing to activate a virtual python 
environment in the future.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

### Initial Setup
When you first run the application it will setup two items in the root of the application folder. The first, if not 
already present, will be a *.\logs* folder. The application is very *"chatty"* logging calls to, if not all, almost all 
functions to help with the inevitable troubleshooting as the API matures. I'm also not a professional programmer, so I'm 
sure I have done things that would make a normal programmer want to kill themselves. The excessive logging helps those 
folks track down what crazy thing I did and fix their setup from my poor design decisions.

The second item that the application will create in the root folder is a *settings.json* file that will store all 
the connection information and global settings for the application. The settings can be accessed from the **Options** 
menu within the application, so there should be no need to access or change this file from outside the application. 

<p align="center">
<img src="images\app_settings_1.png" width="300"/> 
<img src="images\app_settings_2.png" width="300"/>
</p>

<span style="font-size:10px;">
<p align="center">
Examples of the application settings dialog. View of the settings dialog with the Zero-Crossing Isosurface 
reconstruction method selected (Left) . View of the settings dialog with the Marching Cubes surface reconstruction selected 
showing the options to set the 'x' and 'y' pixel size (set to 1 x 1 pixel resolution) (Right) 
</p>
</span>

The application level settings are organized in two sets.
1. DICOM Settings
2. MapRT Settings

#### DICOM Settings

<span style="color:#0055ff"><b>Data Directory</b></span>

The DICOM data directory is where you can have your favorite DICOM SCP drop DICOM RT plan and structure set files 
so that the application can validate them using the MapRT API.

<span style="color:#0055ff"><b>Arc Check Resolution</b></span>

The angular resolution at which to validate an arc treatment field from the DICOM RT plan file.

<span style="color:#0055ff"><b>Surface Reconstruction Method</b></span>

The reconstruction method that will be used to generate the DICOM surface mesh from the DICOM RT structure contours.

- *Zero Crossing* (Default) - Uses a signed distance image to determine the zero-crossing isosurface (fastest)
- *Marchine Cubes* - Using a binary volume image generated from the structure contours (slower recon)
- *Contour Isosurface* - Using a binary volume image generated from the structure contours (slower recon)


The *Marching Cubes* and *Contour Isosurface* reconstruction methods allow the user to determine the pixel resolution in 
the *x* and *y* dimensions (the z dimension is determined form the DICOM RT structure contours). The finer the 
resolution the slower the reconstruction but the closer to the TPS structure volume it will be when generating the 3D 
binary image from which the surface mesh is generated.

<span style="color:#0055ff"><b>Contours to keep</b></span>

The contours to include in the surface generation. In DICOM RT (Radiotherapy) Structure Set files, contour 
orientation—specifically whether the points are ordered clockwise (CW) or counter-clockwise (CCW)—is significant because 
it indicates the interior (filled area) versus the exterior (excluded area) of the contour.

- *CCW* (Default) - Keeps only the contours with counter-clockwise orientations (i.e. outer boundaries)
- *CW* - Keeps only the contours with clockwise orientation (i.e. holes)
- *ALL* - Keeps all contours with no regard for orientation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### MapRT Settings

<span style="color:#0055ff"><b>URL</b></span>

The institution's specific URL for the MapRT API install including the port that the API runs on.

<span style="color:#0055ff"><b>Token</b></span>

The institution's specific *Bearer Token* used in authentication of API calls. This will be provided by Vision RT and is 
specific to you instance of MapRT.

<span style="color:#0055ff"><b>User Agent</b></span>

The institution's version specific user agent for the MapRT API. At the time of this documentation, the version should 
be *VisionRT.Integration.Saturn/2.0.0*

<p align="center">
<img src="images\ping_test.png" width="300"/>
</p>

<span style="font-size:10px;">
<p align="center">
Successful Ping of the MapRT API after proper configuration of the API settings
</p>
</span>

After all MapRT API settings are entered into the application settings dialog the user can test the MapRT API connection 
to see if all the settings are properly configured for the MapRT API endpoint. Clicking the **OK** button will save all 
the changes made to the application settings. Clicking the **Cancel** button will discard all changes made. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Opening DICOM Files

<p align="center">
<img src="images\dicom_open_1.png" width="250"/> 
<img src="images\dicom_open_2.png" width="250"/>
<img src="images\dicom_open_3.png" width="250"/>
</p>

<span style="font-size:10px;">
<p align="center">
Examples of the interface after opening a patient's DICOM RT Plan and Structure Set files using different surface 
reconstruction methods. (Left) Zero-Crossing Isosurface, (Center) Marching Cubes with 1x1 pixel resolution, and 
(Right) Marching Cubes with 3x3 pixel resolution.
</p>
</span>

<p align="center">
<img src="images\dicom_open_0.png" width="800"/>
</p>

<span style="font-size:10px;">
<p align="center">
Interface with DICOM RT information displayed in the <b>Patient Context</b> section. 
</p>
</span>

Opening DICOM RT files from the **File->Open->DICOM RT Files** menu will populate the *Patient Context* section of the 
interface with the information from the DICOM RT Plan and DICOM RT Structure Set.
You will be presented with
- Patient Medical Record Number (MRN)
- Patient First Name
- Patient Last Name
- Course ID (*F1* if loaded from DICOM RT file - **ESAPI integration will populate when implemented**)
- Plan ID (Single unselectable option for DICOM RT file loading - **multiple plans available through ESAPI**)
- Isocenter coordinate (for the selected plan)
- Body Structure (The Body or External structure but you may need to select another more appropriate structure from the 
dropdown for things like *BH Body* or *FB Body*)
- Beams (all fields from the DICOM Plan being validated)

The selected body structure is processed, and the surface mesh is generated with the reconstruction method selected in 
the application settings. The resulting surface mesh can be explored in the 3D viewer. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### 3D View Manipulation and Mouse Controls
The camera orientation can be manipulated using the camera orientation widget in the upper right corner of the 3D view 
by clicking on the axis from which you would like to view the 3D model. The left mouse button will allow you to rotate 
the view around the camera focus point. Pressing and holding the middle mouse button will allow you to pan the model 
around the 3D view port. Pressing and holding the right mouse button and dragging will allow you to zoom in and out on 
the model.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Visual Settings

<p align="center">
<img src="images\3D_view_settings_0.png" width="800"/>
</p>

<span style="font-size:10px;">
<p align="center">
3D view port with adjusted color settings
</p>
</span>

All of the visual settings for the 3D view can be customized from the **3D View Settings** tab. Surface colors, laser 
colors and the view port background color can all be set for the session (unfortunately they are not *"sticky"* right 
now). The laser colors are linked across surfaces and can be customized. The laser opacity is also customizable, 
however, the laser opacity is tied to the surface opacity on which it is projected. This helps to avoid confusion by 
forcing the laser lines projected on an associated surface to fade away with that surface as its opacity is adjusted 
to a value of 0.  

<p align="center">
<img src="images\example_save.png" width="300"/>
<img src="images\example_save.bmp" width="300"/>
</p>

<span style="font-size:10px;">
<p align="center">
Examples of a .png image saved with the 3D model alone (Left) and a .bmp image saved with the axis orientation and view 
orientation widgets visible (Right). 
</p>
</span>

The 3D scene can be manipulated and viewed from any preferred angle or axis direction. The axis orientation widget and 
the view orientation widget can be hidden from the 3D view settings page. It is possible to save the 3D view for use in 
presentations or other outside documentation. The user can save the 3D view as a *.png* image which will set the  
viewport background to transparent or as a .bmp image which will preserve the view as seen on the screen. The axis and 
view orientation widgets will be saved in the image if visible within the view port. If the user does not desired to see
them in the output image they should be turned off the widgets prior to saving the image.


<!-- For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Connection to the MapRT API

#### Surface Alignment Checks
<p align="center">
<img src="images\maprt_connect_0.png" width="800"/>
</p>

<span style="font-size:10px;">
<p align="center">
Image showing a populated MapRT Context section. Information is populated for the currently active <b>Patient Context</b>
or for the MRN provided after the <b>Fetch Data</b> button is pressed.
</p>
</span>

MapRT data for the currently active Patient Context can be retrieved from the MapRT API by clicking the *Fetch Data* 
button. The MRN from the active Patient Context will be used to query the MapRT API and retrieve not only the 
patient-specific surfaces but also the room / machine geometries available for clearance map generation. When 
the surface calls are completed, the MapRT surface meshes that are returned are cached for visual display within the 
3D view using the DICOM coordinate system.

>**Note:** The MapApp converts all coordinates to the native DICOM coordinate system of IEC-61217. All corrections to 
>MapRT surfaces and visual verification of the registration between MapRT and your DICOM structures take place in the 
> DICOM coordinate system. This become important when comparing DICOM structures to MapRT surfaces or [exporting MapRT 
> surfaces to DICOM](#experimental-synthetic-cTs) which will be discussed later in the documentation

Visual verification of the registration between the DICOM body structure and the MapRT surface is crutial to the proper 
use of the clearance map generated using the MapRT surface captured during CT simulation. If, as in the case represented 
by the image above, the DICOM body structure and the MapRT surface are properly aligned, the clearance map can be 
trusted to provide an accurate understanding of the available beam arrangements during planning. However, if the DICOM 
body structure and the MapRT surface are not properly aligned (as shown in the image below), the clearance map cannot 
be trusted to accurately reflect the conditions during delivery and may actually cause collisions rather than help the 
user avoid them.

<p align="center">
<img src="images\misalignment_0.png" width="400"/>
<img src="images\misalignment_1.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
Misaligned DICOM surface with the MapRT surface (Left). Corrected MapRT surface now aligned with the DICOM body surface 
(Right)
</p>
</span>

If a DICOM to MapRT surface misalignment is identified, MapApp will allow the user to correctly align the MapRT 
surface to the DICOM RT planning surface using the *Correction* section of the MapRT Context. The user can then resubmit 
the corrected isocenter coordinate to the MapRT API for generation of a corrected clearance map.

> Aligning the MapRT surface to the DICOM body structure is a manual process. It is the responsibility of the user to 
> ensure that the alignment is done properly to allow for confidence in using the resulting clearance map for planning. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Virtual Simulations

<p align="center">
<img src="images\maprt_connect_1.png" width="400"/>
<img src="images\maprt_connect_2.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
Image showing patient look-up dialog with associated patient orientation selection dropdown (Left). Image showing result 
of loading a patient directly from MapRT API without an active Patient Context.
</p>
</span>

If there is no active Patient Context to work from (i.e. at CT simulation prior to start of planning), the MapApp will 
prompt the user for the patient's MRN and the orientation of the patient via a small dialog. The orientation is used to 
convert the MapRT surface coordinates into the standard DICOM coordinate system (IEC-61217).

Patients loaded directly from MapRT API without an active Patient Context loaded from DICOM RT files will have a few 
distinguishing features. You will note from the right-hand image above that a *MapRT Preview* Patient Context is 
generated and populated in the Patient Context section. The isocenter is placed at <0, 0, 0> which mimics the preview 
plan in the native MapRT application. The isocenter is easily identified visually using the laser projections on the 
MapRT surface in the 3D view. The isocenter can be adjusted to any location using the **Correction** section within the 
MapRT Context section of the UI. Placing the isocenter on the patient surface within the 3D view will allow you to 
check the clearance map at that location. 

**To check the clearance map for the current Isocenter location** 
1. Click the **Get Map** button when you are satisfied with the visual location of isocenter as indicated by the virtual 
laser system. 
2. This will populate the clearance map in the *Map View* tab. 
> Clearance maps are cached in the MapApp unlike in the native MapRT application. This means you are able to check 
> multiple isocenter locations very rapidly due to the threaded nature of the API calls. As the clearance maps are 
> calculated and returned from the API (first as low resolution maps then as high resolution maps) the clearance map 
> graph is updated with the latest information. 
3. Each clearance map, with the settings used to generate it, are stored in the clearance map dropdown just below the 
clearance map graph for easy review. The label in the dropdown is configured as follows **[Machine] -- [Surface] -- 
[Isocenter coordinate] -- [Couch Buffer] -- [Patient Buffer]** to help you locate the proper clearance map.
>Note: The 3D visual of the isocenter is currently not linked to the dropdown selection.

This workflow is helpful in testing isocenter / patient positioning combinations prior to completing a CT simulation of 
the patient. By capturing a surface of the patient and pulling that surface into the MapApp prior to initiating the CT 
you can rapidly verify the patient's position will not contribute to undue collision risk prior to simulation.

<p align="center">
<img src="images\virtual_sim_0.png" width="400"/>
<img src="images\virtual_sim_1.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
Isocenter / Clearance Map combination at isocenter location #1
</p>
</span>

<p align="center">
<img src="images\virtual_sim_2.png" width="400"/>
<img src="images\virtual_sim_3.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
Isocenter / Clearance Map combination at isocenter location #2
</p>
</span>

<p align="center">
<img src="images\virtual_sim_4.png" width="800"/>
</p>

<span style="font-size:10px;">
<p align="center">
Cached Clearance Maps can be retrieved by selecting them in the dropdown below the clearance map grap
</p>
</span>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Experimental Synthetic CTs

There may be times when you would like to use the MapRT surface for things other than clearance map generation. This can 
include things like generating training materials, virtual phantoms, capturing test patients, transfer to AlignRT for 
use during setup taking advantage of MapRT's larger surface, testing and comparison to other collision detection systems 
like ClearCheck from Radformation and the list goes on and on.

To achieve many of these tasks, the MapRT surface often needs to be accessible to the Treatment Planning System (TPS). 
There have been a number of attempts to get the surface meshes generated from these optical systems into the TPS in the 
past, but there are a number of techinical challenges to doing this and getting a usable result. The MapApp allows the 
user to move the equivalent of the MapRT surface into the TPS by voxelating the surface and converting it into a 3D image 
stack. The 3D image stack is converted into a series of DICOM CT images that can then be imported into the TPS and 
recontoured using the native tools in the TPS. This avoids many, if not all, of the direct surface mesh to contour 
conversion issues others have reported.

Using this method can reduce the surface resolution of the captured MapRT surface so studies on accuracy between 
collision detection tools need to account for this. However, the utility of the surfaces generated in the TPS using this 
method is often worth the minimal loss in surface accuracy.

To generate a synthetic CT in the MapApp you need to pull the surface information for a patient or phantom from the MapRT 
API or open a *.obj* file from your local hard drive. When the surface mesh is finished being processed the surface will 
render in the main 3D viewer where you can inspect its quality. When you are satisfied with the mesh selected use 
**File->Export->MapRT Surface to DICOM** utility to select the region of the surface you wish to convert to a synthetic 
CT.

<p align="center">
<img src="images\export_dicom_0.png" width="400"/>
<img src="images\export_dicom_1.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
MapApp Export Surface to DICOM Utility with full surface (Left). Truncated surface removing the legs and everything 
below the table surface (Right).
</p>
</span>

The size of the resulting synthetic CT will be dependent on the settings used to convert the surface to image data. 

**Surface to DICOM Export Settings**

<span style="color:#0055ff"><b>Voxel Size</b></span>

The voxel size will significantly impact the overall quality of the surface in the TPS (as the vovel size increases the 
detail / quality of the surface will decrease). If the voxel size is too small the surface may have wholes that will 
reduce the quality of the surface in the TPS. I would recomend a voxel size of 3mm if you are exporting only the surface 
voxels but experimentation will tell you what is best for your use case.

<span style="color:#0055ff"><b>Fill Down</b></span>

When *"Fill Down"* is enabled it is important to set the bounds so that the bounding box clips at the surface of the CT 
table. Since MapRT surfaces are open (i.e. not water tight surface meshes) filling down simply uses the surface "Y" 
coordinate (IEC-61217) as the vertical max and fills all voxels between the surface and the minimum bounds (table 
surface) with the same voxel value. If the bounding box is not set at the table surface the resulting CT volume will 
have an artificial height in the TPS if aligned to a support structure like a couch top.

<span style="color:#0055ff"><b>Gaussian Smooth</b></span>

Currently only 3D Gaussian smoothing is available to smooth the pixel values after image generation. This supplies a 
minimum anount of "whole filling" for low quality surfaces. The associated **Sigma** value simply sets the width of the 
gaussian window for smoothing so if you have larger wholes and want a smoother surface you will need to increase the 
sigma value at the detriment of the overall surface quality.

<p align="center">
<img src="images\export_dicom_0.png" width="800"/>
<img src="images\export_dicom_2.png" width="400"/>
<img src="images\export_dicom_3.png" width="400"/>
</p>

<span style="font-size:10px;">
<p align="center">
MapApp Export Surface to DICOM (Top) without (Left) Fill Down selected with (Right) Fill Down selected while holding all other 
settings the same (3mm voxel gaussian smooth with sigma=1
</p>
</span>


I would recommend playing with the various settings on surfaces of different qualities to see what can be achieved. 
There are a bunch of other morphological operations that can be used to clean up these surfaces prior to and even after 
 voxelation, so feel free to dig in and write up a few additional routines and if you come up with a good one share it 
with the community.

When you hit **OK** to close the utility it will save the synthetic CT to the configured DICOM directory that you have 
set in your settings file under a folder named with the patient MRN followed by the voxel size you selected.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Connect the application to ESAPI so that the application can access active plan contexts in Eclipse
- [ ] Work on implementation of additional 3D visualization and export capabilities
- [ ] Implement additional surface corrections, couch indexing, and couch centering capabilities for Varian linacs
- [ ] Improve code commenting
- [ ] Improve this documentation

See the [open issues](https://github.com/tallhamer/MapApp/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any 
contributions you make are **greatly appreciated**.

That being said I am a novice at these things so if you are better at github than I am feel free to send suggestions 
and How To's to me on what I need to do to help make contributing an easier process.

If you don't code but have a suggestions that could make this better or more user friendly, please create  open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

Do you want  to be listed here? You know you do! Send me an email or suggestion on how we can better expand the use of
this new API within our clinical practice and I will add you here when it is implemented.


<!-- LICENSE -->
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Michael J Tallhamer M.Sc DABR - [Michael.Tallhamer@AdventHealth.com](mailto:Michael.Tallhamer@AdventHealth.com)

Project Link: [https://github.com/tallhamer/MapApp.git](https://github.com/tallhamer/MapApp.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
Thanks to the following for your suggestions, testing, and assistance in getting this project up and running for the 
community to learn from and continue to develop here or on their own.

* Anton Eagle M.Sc. DABR - Medical Physicist AdventHealth - Parker
* Adi Robinson PhD DABR - Medical Physicist AdventHealth - Celebration
* Piotr Cendrowski - Senior Vice President, Research & Development Vision RT
* Andrzej Wawrzynczyk - Vision RT
* Christopher Rausch - Vision RT

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[project-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-3.12.9-blue?logo=python&logoColor=white
[Python-url]: https://www.python.org/
[PySide6]: https://img.shields.io/badge/PySide6-Qt%20for%20Python-41cd52?logo=qt&logoColor=white
[PySide6-url]: https://doc.qt.io/qtforpython-6/
[app-settings-screenshot]: images\app_settings.png
