# VMware Avi Load Balancer: Python Test Automation Framework

This project implements a Python-based, configuration-driven, and parallelized test automation framework for interacting with the VMware Avi Load Balancer (Mock) API.

## Objectives Met

The framework is designed to fulfill the following requirements:

* *Language:* Built entirely in Python.
* *Configuration:* All parameters (endpoints, credentials, test flow) are stored and dynamically parsed from config.yaml.
* *Parallelism:* Utilizes Python's concurrent.futures.ThreadPoolExecutor to execute multiple test cases concurrently.
* *Modularity:* Logic is separated into main.py (orchestration) and avi_api_utils.py (helpers, API calls, and mocks).
* *Workflow:* Implements the required 4-stage execution model (Pre-Fetcher, Pre-Validation, Task/Trigger, Post-Validation).
* *Mocks:* Includes stubbed methods for SSH and RDP.

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.x installed.
* The required Python libraries.

### 2. Setup and Installation

1.  *Clone/Download:* Place all files (main.py, avi_api_utils.py, config.yaml, requirements.txt) into a single directory.
2.  *Install Dependencies:* Open your terminal in the project directory and run:
    bash
    pip install -r requirements.txt
    

### 3. Configuration

The core of the framework is the **config.yaml** file.

*Crucial Step: Update the Bearer Token*

Before execution, you *must* update the API token in config.yaml with your current active session token (e4f1aa4a-2f43-40c6-868d-823bb2633b64).

```yaml
# config.yaml Snippet
api:
  token: "<token>" # Paste your token here 
  headers:
    # ...
    Authorization: "Bearer <token>" # Paste your token here
