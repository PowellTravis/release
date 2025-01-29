# **OpenCHAMI Release Policy**

OpenCHAMI is a microservices-based High-Performance Computing (HPC) system manager designed to support HPC-specific applications while integrating third-party open-source containers for non-HPC-specific functionality. This release policy outlines the versioning, support, and update mechanisms for OpenCHAMI’s releases and microservices.

## **Release Composition and Attestation**

Each OpenCHAMI release consists of a collection of containers that:

- Are identified by a unique **release version**.
- Are **cryptographically signed** and can be **attested** using known versions, SHA hashes, and signatures.
- Include both OpenCHAMI’s custom microservices and selected third-party open-source containers.
- Are packaged and delivered in a way that ensures reproducibility and security.

## **Supported Deployment Methods**

To accommodate various environments, OpenCHAMI supports multiple deployment options:

- **RPM Packages**: Built for **RHEL** and **SUSE**-based systems, utilizing **Podman quadlets** for container deployment.
- **Helm Charts**: Provided for Kubernetes-based deployments.
- **Docker Compose**: Available for simpler or local deployments.

## **Release Cadence**

### **Major Releases**

- Major releases introduce **new features, architecture changes, or breaking changes**.
- Each major release is supported for **three years**, contingent on the support lifecycle of third-party dependencies.
- Major releases are identified using **semantic versioning** (e.g., `2.0.0`).

### **Quarterly Release Updates**

- Updates within a major release stream are delivered on a **quarterly basis**.
- These updates include **security patches, bug fixes, and incremental feature improvements**.
- Quarterly updates **do not introduce breaking changes** and are versioned as **minor or patch releases** (e.g., `2.1.0`, `2.1.1`).

### **Continuous Microservice Development**

- Each microservice within OpenCHAMI follows **independent versioning**.
- Microservices may be **updated more frequently** than the main quarterly release cycle.
- Microservice updates are **backported** into quarterly releases as necessary.

## **Security & Support Commitment**

- OpenCHAMI commits to providing **best-effort support** for three years per major release.
- Support includes **critical bug fixes, security patches, and compatibility updates**.
- The availability of updates for third-party open-source containers depends on their respective maintainers.

## **Upgrade and Compatibility Strategy**

- **Backward compatibility** is maintained within a major release stream where possible.
- **Upgrade paths** will be documented, including required migrations for major releases.
- **Automated upgrade scripts** may be provided to simplify the transition between versions.

## **End-of-Life (EOL) Policy**

- After three years, a release enters **end-of-life status**, meaning:
  - No further updates or security patches will be provided.
  - Users are encouraged to **migrate to a newer release** before the EOL date.
  - Any third-party dependencies that reach EOL within the five-year window may necessitate early updates or discontinuation of support.

## **Release Verification and Distribution**

- Each release is **cryptographically signed**, and images are published with **verifiable signatures**.
- OpenCHAMI artifacts (containers, RPMs, Helm charts, Docker Compose files) are distributed via:
  - **Official container registries** (e.g., Quay.io, Docker Hub).
  - **Package repositories** for RHEL and SUSE-based distributions.
  - **Helm chart repositories** for Kubernetes deployments.
  - **GitHub or other official distribution channels**.