# Cires-Technologies-SOC
# Mini SOC Deployment with Wazuh on Docker Swarm

## Project Overview
This repository contains the implementation of a Mini SOC environment deployed on **Azure** using **Docker Swarm**. The SOC includes **Wazuh Manager, Indexer, and Dashboard**, running with HTTPS and persistent storage. Deployment is automated with **Ansible playbooks**.  

**Key Features:**  
- HA Docker Swarm cluster (3 managers, 2 workers)  
- Overlay network for Wazuh services (`wazuh-net`)  
- Persistent storage for Wazuh data  
- HTTPS access to the Wazuh Dashboard  
- Reproducible deployment via Ansible  

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
- **Ansible playbook** handles:  
  - Swarm initialization/join  
  - Overlay network creation  
  - Wazuh stack deployment  
  - TLS/HTTPS setup  

**Architecture Diagram Placeholder:**  
![Architecture Diagram](docs/architecture.png)

---

## Prerequisites

- Azure subscription & VMs  
- Docker 20.x+ installed on all nodes  
- Ansible 2.9+ on management VM  
- GitHub self-hosted runner (optional for CI/CD)  
- Python, Trivy, and Chrome/Chromedriver (if testing implemented)  
- Network connectivity between subnets  

---

## Deployment Steps

1. **Initialize Swarm**  
```bash
docker swarm init --advertise-addr <MANAGER_IP>
