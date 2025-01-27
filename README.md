# OpenCHAMI Releases

OpenCHAMI is a system manager/provisioner for securely managing HPC clusters.  It has a microservices architecture leveraging third party tools for non-HPC specific applications.  The HPC-specific features are delivered through a 

## Features

* Redfish-based automatic compute node discovery
* Continuously validated inventory with secure machine identity
* Inventory-driven operations with support for automatic DNS and DHCP
* API Integrations for configuration management tooling like Ansible, Terraform, and Kubernetes ClusterAPI
* Cloud-Init server with HPC features and optional Wireguard/TPM security
* Operating System Agnostic
* Deployable with Kubernetes, Docker Compose, Podman Quadlets, and Linux SystemD
* OIDC Authentication with discretionary access control at the API level
* Short-lived, narrowly scoped, renewable JWTs for admin access



## Latest Microservice Releases

| Repository | Release | Container | Attestations |
| :---: | :----: | :----: | :------: | 
| [OpenCHAMI/BSS](https://github.com/openchami/bss) | [![BSS Release](https://badgen.net/github/release/openchami/bss/stable)](https://github.com/openchami/bss/releases) | [ghcr.io/openchami/bss](https://github.com/OpenCHAMI/bss/pkgs/container/bss) | [Attestations](https://github.com/OpenCHAMI/bss/attestations) |
| [OpenCHAMI/SMD](https://github.com/openchami/smd) | [![SMD Release](https://badgen.net/github/release/openchami/smd/stable)](https://github.com/openchami/smd/releases) | [ghcr.io/openchami/smd](https://github.com/OpenCHAMI/smd/pkgs/container/smd) | [Attestations](https://github.com/OpenCHAMI/smd/attestations) |
| [OpenCHAMI/cloud-init](https://github.com/openchami/cloud-init) | [![Cloud-Init Release](https://badgen.net/github/release/openchami/cloud-init/stable)](https://github.com/openchami/cloud-init/releases) | [ghcr.io/openchami/cloud-init](https://github.com/OpenCHAMI/cloud-init/pkgs/container/cloud-init) | [Attestations](https://github.com/OpenCHAMI/cloud-init/attestations) |
| [OpenCHAMI/coresmd](https://github.com/openchami/coresmd) | [![Coresmd Release](https://badgen.net/github/release/openchami/coresmd/stable)](https://github.com/openchami/coresmd/releases) | [ghcr.io/openchami/coresmd](https://github.com/OpenCHAMI/coresmd/pkgs/container/coresmd) | [Attestations](https://github.com/OpenCHAMI/coresmd/attestations) |
| [OpenCHAMI/magellan](https://github.com/openchami/magellan) | [![Magellan Release](https://badgen.net/github/release/openchami/magellan/stable)](https://github.com/openchami/magellan/releases) | [ghcr.io/openchami/magellan](https://github.com/OpenCHAMI/magellan/pkgs/container/magellan) | [Attestations](https://github.com/OpenCHAMI/magellan/attestations) |
