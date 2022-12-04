<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/UniCT-ARSLab/PepperGateway">
    <img src="images/logo.png" alt="Logo" width="250" height="250">
  </a>

<h3 align="center">Pepper Gateway</h3>

  <p align="center">
    Project Description
    <br />
    <a href="https://github.com/UniCT-ARSLab/PepperGateway"><strong>Explore the Docs</strong></a>
    <br />
    <br />
    <a href="https://github.com/UniCT-ARSLab/PepperGateway">View Demo</a>
    ·
    <a href="https://github.com/UniCT-ARSLab/PepperGateway/issues">Report Bug</a>
    ·
    <a href="https://github.com/UniCT-ARSLab/PepperGateway/issues">Request Feature</a>
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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Summary
Repository contains the project for my BsC Degree. It is based on the implementation of a gateway for the Pepper robot, which can establish a point of contact between the user and the robot itself. In this way, the user can interface with the robot, order movements and/or information, or more generally request tasks. The latter are carried out completely autonomously by the robot.



### Built With

[![Python][Python.org]][Python.org]



<!-- GETTING STARTED -->
## Getting Started

<!-- This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps. -->


### Prerequisites

It is necessary to add `naoqi`, a third-party python package for using qi drivers. Download Python SDK for Pepper [here](http://doc.aldebaran.com/2-5/dev/python/install_guide.html).
After downloading the SDK - and cloned this repository - move it inside the root folder (e.g. `mv pynaoqi PepperGateway/`).

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/UniCT-ARSLab/PepperGateway.git
   ```
2. Build Docker Image
   ```sh
   make build
   ```
3. Run container. Before run, make sure you have changed the volume path on the Makefile.
   ```sh
   make run
   ```



<!-- USAGE EXAMPLES -->
### Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- LICENSE -->
## License
Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/UniCT-ARSLab/PepperGateway](https://github.com/UniCT-ARSLab/PepperGateway)

<p align="right">(<a href="#readme-top">Back to 🔝</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/UniCT-ARSLab/PepperGateway/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/UniCT-ARSLab/PepperGateway/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/UniCT-ARSLab/PepperGateway/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/UniCT-ARSLab/PepperGateway/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/UniCT-ARSLab/PepperGateway/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=jquery&logoColor=white
