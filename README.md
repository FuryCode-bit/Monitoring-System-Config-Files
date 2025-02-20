<!-- Project Monitoring-System-Config-Files: https://github.com/FuryCode-bit/Monitoring-System-Config-Files -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/FuryCode-bit/Monitoring-System-Config-Files">
    <img src="readme/ua.png" alt="Logo" height="80">
  </a>

  <h3 align="center">Threat Detection System with Tolerance Mechanisms</h3>

  <p align="center">
    <br />
    <a href="https://github.com/FuryCode-bit/Monitoring-System-Config-Files"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://github.com/FuryCode-bit/Monitoring-System-Config-Files">View Demo</a> -->
    ·
    <a href="https://github.com/FuryCode-bit/Monitoring-System-Config-Files/issues">Report Bug</a>
    <!-- ·
    <a href="https://github.com/FuryCode-bit/Monitoring-System-Config-Files/issues">Request Feature</a> -->
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][project-screenshot]

<!-- OBJECTIVE -->
### Objective

The objective of this project is to provide an effective system for the detection and mitigation of digital threats in real time. Developed as part of the Master's in Cybersecurity at the University of Aveiro, it aims to create a robust monitoring system capable of identifying potential attacks and implementing tolerance mechanisms to actively respond to them. The system is designed to detect and mitigate threats using a combination of security sensors, event correlation engines, and automatic response modules.

<!-- ARCHITECTURE -->
## System Architecture

This system operates in a virtualized environment using Proxmox and is distributed across 6 virtual machines and 7 Linux containers. The core component of the system is the Security Information and Event Management (SIEM), which is assisted by various exporters and central dashboards.

The system architecture follows a distributed model to ensure redundancy, scalability, and resilience. It is divided into four main zones:

 * **North Zone**: Data collection and visualization, using Prometheus and Grafana for metric gathering and dashboard visualization.
 * **Central Zone**: Core control center that manages event correlation and response, powered by Wazuh for monitoring and threat analysis.
 * **South Zone**: A simulation environment where various attack scenarios are tested, including malware, botnets, and denial-of-service (DoS) attacks.
 * **West Zone**: Hosts auxiliary services, including temperature monitoring systems, to ensure the overall health of the infrastructure.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TOLERANCE MECHANISMS -->
## Tolerance Mechanisms

To enhance the robustness and fault tolerance of the system, several mechanisms were implemented to ensure its resilience even in the face of threats and failures. These include:

 * **Moving Target Defense (MTD)**: A dynamic machine rotation system prevents static analysis of the temperature collection nodes by frequently changing the containers running the service, thus ensuring continuous operation despite potential Denial-of-Service (DoS) attacks.
 * **Load Balancing** with Consul and Fabio: This mechanism ensures high availability by distributing traffic across multiple nodes, preventing service interruptions even during spikes or failures.
 * **Distributed Consensus** with Raft: By utilizing the Raft consensus protocol, the system ensures reliable decision-making and data integrity in a distributed environment, with automatic leader election to handle node failures.

<!-- FEATURES -->
## Key Features

 * **Real-time threat** detection using security sensors that gather logs from servers, network traffic, authentication events, and application activity.
 * **Event correlation** engine to identify sophisticated threats by analyzing behavior patterns across multiple data sources.
 * **Automatic mitigation** response, reducing reaction time to incidents and preventing the propagation of attacks.

<!-- LICENSE -->
## License

Distributed under the Apache License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/FuryCode-bit/Monitoring-System-Config-Files.svg?style=for-the-badge
[contributors-url]: https://github.com/FuryCode-bit/Monitoring-System-Config-Files/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/FuryCode-bit/Monitoring-System-Config-Files.svg?style=for-the-badge
[forks-url]: https://github.com/FuryCode-bit/Monitoring-System-Config-Files/network/members
[stars-shield]: https://img.shields.io/github/stars/FuryCode-bit/Monitoring-System-Config-Files.svg?style=for-the-badge
[stars-url]: https://github.com/FuryCode-bit/Monitoring-System-Config-Files/stargazers
[issues-shield]: https://img.shields.io/github/issues/FuryCode-bit/Monitoring-System-Config-Files.svg?style=for-the-badge
[issues-url]: https://github.com/FuryCode-bit/Monitoring-System-Config-Files/issues
[license-shield]: https://img.shields.io/github/license/FuryCode-bit/Monitoring-System-Config-Files.svg?style=for-the-badge
[license-url]: https://github.com/FuryCode-bit/Monitoring-System-Config-Files/blob/master/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/bernardeswebdev

[project-screenshot]: readme/ssle.png
