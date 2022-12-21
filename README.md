<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
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
Repository contains the project for my BsC Degree. It is based on the implementation of a gateway for the Pepper robot, which can establish a point of contact between the user and the robot itself. In this way, the user can interface with the robot, order movements and/or information, or more generally request tasks. The latter are carried out completely autonomously by the robot.
    <br />
    <br />
    <br />
    <a href="https://github.com/UniCT-ARSLab/PepperGateway">View Demo</a>
    ·
    <a href="https://github.com/UniCT-ARSLab/PepperGateway/issues">Report Bug</a>
    ·
    <a href="https://github.com/UniCT-ARSLab/PepperGateway/issues">Request Feature</a>
  </p>
</div>

#### Built With
`Python 2.7`



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

First you need to download a Python SDK for Pepper, [PyNaoqi](http://doc.aldebaran.com/2-5/dev/python/install_guide.html).
  ```sh
  make build
  ```

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
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->

_For more examples, please refer to the [Documentation](https://example.com)_



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


<!-- LICENSE -->
## License
Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/UniCT-ARSLab/PepperGateway](https://github.com/UniCT-ARSLab/PepperGateway)
