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
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">MapApp</h3>

  <p align="center">
    An example project to illustrate some of the <a href="https://visionrt.com/our-solutions/maprt-api/">MapRT API</a> integration possibilities. The application is a standalone 
    python application that connects to the MapRT API and provides DICOM plan validation and clearance map visualization.
    <br /> 
    <br />
    While the application seeks to simply show integration strategies with MapRT's API it does provide some useful 
    clinical features that users may find useful in clinical practice. The application is provided MIT license and 
    should be used in clinical practice at the user's own risk.  
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br /><br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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
3. Navigate the the new *Scripts* folder and activate the new virtual environment using the proper active script.
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
   
4. Clone the github repo for this project.
    ```sh
      git clone https://github.com/tallhamer/MapApp.git
    ```
5. With the virtual python environment activated, navigate to the location of the cloned git repo and install the project 
   dependencies using the requirement.txt file.
    ```sh
      pip install -r requirements.txt
    ```
After all of the python libraries have been successfully installed, you should be able to simply type the following from 
the activated virtual python environment to launch the application.
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
      pyinstaller map_app.py --paths=FullPathToRepoFolder -D --hidden-import=skimage._shared.geometry 
    ```
The result should be a *dist* folder with a subfolder named *map_app*. You can move the *map_app* folder to any location 
and run the map_app.exe from that folder to use the application without needing to activate a virtual python environment 
in the future

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

### Initial Setup
When you first run the application it will setup to locations in the root of the application folder. The first, if not 
already present, will be a *.\logs* folder. The application is very *"chatty"* logging calls to, if not all, almost all 
functions to help with the inevitable troubleshooting as the API matures. I'm also not a professional programmer, so I'm 
sure I have done things that would make a normal programmer want to kill themselves. The excessive logging helps those 
folks track down what crazy thing I did and fix their setup from my poor design decisions.

The second item that the application will create upon first run is an initial settings file that will store all the 
connection information and global settings for the application. The settings can be accessed from the **Tools** menu 
within the application so there should be no need to access or change this file from outside of the application. 

<p align="center">
<img src="images\app_settings_1.png" width="300"/> 
<img src="images\app_settings_2.png" width="300"/>
</p>

The application level settings are organized in two sets.
1. DICOM Settings
2. MapRT Settings

#### DICOM Settings

Data Directory
:  The DICOM data directory is where you can have your favorite DICOM SCP drop DICOM RT plan and structure set files 
so that the application can validate them using the MapRT API.

Arc Check Resolution
:  The angular resolution at which to validate an arc treatment field from the DICOM RT plan file.

Surface Reconstruction Method
:  The reconstruction method that will be used to generate the DICOM surface mesh from the DICOM RT structure contours.

- Zero Crossing Isosurface (Default) - Uses a signed distance image to determine the zero isosurface (fastest)
- Marchine Cubes - Using a binary volume image generated from the structure contours (slower recon)
- Contour Isosurface - Using a binary volume image generated from the structure contours (slower recon)


The Marching Cubes and Contour Isosurface reconstruction methods alow the user to determine the pixel resolution in the 
**x** and **y** dimensions (z dimention is determines form the DICOM RT structure contours). The finer the resolution 
the slower the reconstruction but the closer to the TPS structure volume it will be when generating the 3D binary image 
from which the surface is generated.

Contours to keep
:  The contours to include in the surface generation. In DICOM RT (Radiotherapy) Structure Set files, contour 
orientation—specifically whether the points are ordered clockwise (CW) or counter-clockwise (CCW)—is significant because 
it indicates the interior (filled area) versus the exterior (excluded area) of the contour.

- CCW (Default) - Keeps only the contours with counter-clockwise orientations (i.e. outer boundaries)
- CW - Keeps only the contours with clockwise orientation (i.e. holes)
- ALL - Keeps all contours with no regard for orientation

#### MapRT Settings

URL
:  The institution specific URL for your MapRT API install including the port the API runs on.

Token
:  The institution specific Bearer Token used in authentication of API calls.

User Agent
:  The institution and version specific user agent for the MapRT API

After all of the MapRT settings are entered into the application settings the user can test the MapRT API connection to 
see if all the settings are properly configured for the MapRT API endpoint. Click the **OK** button will save all the 
changes made to the application settings. Clicking Cancel will revert all settings back to the defaults or the original 
settings resulting in all of your changes being lost. 

### Opening DICOM Files

<p align="center">
<img src="images\dicom_open_1.png" width="250"/> 
<img src="images\dicom_open_2.png" width="250"/>
<img src="images\dicom_open_3.png" width="250"/>
</p>

<p align="center">
Examples of opening a DICOM RT Plan and DICOM RT Structure Set file combination using different surface reconstruction 
methods. (Left) Zero-Crossing Isosurface, (Center) Marching Cubes with 1x1 pixel resolution, and 
(Right) Marching Cubes with 3x3 pixel resolution.
</p>









<!-- For more examples, please refer to the [Documentation](https://example.com)_ -->

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

Distributed under the project_license. See `LICENSE.txt` for more information.

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
