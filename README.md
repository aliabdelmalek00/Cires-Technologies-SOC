# Mini SOC Deployment with Wazuh on Docker Swarm

## Project Overview
This repository contains a **fully automated Mini SOC environment** deployed on **Azure** using **Docker Swarm**. The SOC includes **Wazuh Manager, Indexer, and Dashboard**, running with HTTPS and persistent storage. Deployment is orchestrated entirely with **Ansible playbooks**.

**Key Features:**  
- Fully automated deployment via **Ansible playbook**  
- HA Docker Swarm cluster (3 managers, 2 workers)  
- Overlay network for Wazuh services (`wazuh-net`)  
- Persistent storage for Wazuh data  
- HTTPS access to Wazuh Dashboard  

---

## Architecture Overview

**Azure Network Setup:**  
- VNet: `10.10.0.0/16`  
- Subnet `swarm`: `10.10.2.0/24` → Swarm nodes (3 managers + 2 workers)  
- Subnet `management`: `10.10.1.0/24` → GitHub runner & NFS server  

**Docker Swarm Cluster:**  
- Managers: 3 (AZ1, AZ2, AZ3)  
- Workers: 2  
- Overlay network: `wazuh-net`  

**Wazuh Stack:**  
- `wazuh-manager`  
- `wazuh-indexer`  
- `wazuh-dashboard` (HTTPS enabled)  
- Persistent volumes for manager and indexer  

**Deployment Automation:**  
- **Ansible playbook automates the full deployment**, including:  
  - Docker installation (`roles/docker_install`)  
  - Swarm initialization (`roles/init_docker_swarm`)  
  - Manager/worker join (`roles/manager_join_docker_swarm`, `roles/worker_join_docker_swarm`)  
  - NFS mount (`roles/mount_nfs`)  
  - Wazuh stack deployment (`roles/deploy_wazuh`)  

**Architecture Diagram Placeholder:**  
![Architecture Diagram](docs/architecture.png)

---

## Folder Structure

.github/workflows/ # GitHub Actions workflows
ansible/deploy-swarm/
├── inventory/ # Inventory files & group_vars
├── roles/
│ ├── deploy_wazuh/ # Wazuh deployment tasks & templates
│ ├── docker_install/ # Install Docker on nodes
│ ├── init_docker_swarm/ # Initialize Swarm cluster
│ ├── manager_join_docker_swarm/ # Manager join tasks
│ ├── worker_join_docker_swarm/ # Worker join tasks
│ └── mount_nfs/ # Mount NFS volumes
tests/ # Selenium/API tests (optional)

yaml
Copy code

---

## Prerequisites

- Azure subscription & VMs  
- Docker 20.x+ installed (via Ansible role if not present)  
- Ansible 2.9+ on management VM (control node)  
- GitHub self-hosted runner (optional for CI/CD)  
- Network connectivity between subnets  

---

## Deployment

**Run the Ansible playbook to deploy everything automatically:**

```bash
ansible-playbook -i ansible/deploy-swarm/inventory/hosts deploy.yml
This playbook performs:

Docker installation

Swarm initialization & joining of managers/workers

Overlay network creation (wazuh-net)

Deployment of Wazuh stack (manager, indexer, dashboard)

HTTPS/TLS setup

Secrets injection via Ansible Vault / Swarm secrets

Verification:

bash
Copy code
docker node ls
docker stack ls
docker stack ps wazuh
docker service ls
Screenshot Placeholders:

Swarm nodes: docker node ls

Stack deployment: docker stack ps wazuh

Services: docker service ls

Wazuh dashboard: docs/dashboard.png

Access Wazuh Dashboard
URL: https://<dashboard_ip_or_domain>

Username / Password: (configured via secrets)

HTTPS enabled using internal certs or Let’s Encrypt

Secrets & Security
All secrets managed via Github secrets

TLS certificates generated automatically and deployed securely


Validation & Testing
Dashboard accessible via HTTPS

Wazuh services healthy and running (docker service ls)

Optional: Selenium/API tests to verify dashboard and API endpoints

Screenshot Placeholders:

Selenium test results: tests/selenium/results.png

API health check response: tests/api/health.png

Next Steps / Improvements
CI/CD integration via GitHub Actions

Automated image scanning with Trivy

Multi-node Wazuh Indexer cluster for higher HA



yaml
Copy code

---

