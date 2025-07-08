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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-3.12.9-blue?logo=python&logoColor=white
[Python-url]: https://www.python.org/
[PySide6]: https://img.shields.io/badge/PySide6-Qt%20for%20Python-41cd52?logo=qt&logoColor=white
[PySide6-url]: https://doc.qt.io/qtforpython-6/

