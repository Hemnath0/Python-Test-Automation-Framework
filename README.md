# VMware Avi Load Balancer: Python Test Automation Framework

A Python-based, configuration-driven, and parallelized test automation framework for interacting with the *VMware Avi Load Balancer (Mock API)*.

---

## Features

* *Language:* Python 3.x
* *Config-Driven:* Uses config.yaml for endpoints, credentials, and test flow.
* *Parallel Execution:* Runs multiple tests concurrently with ThreadPoolExecutor.
* *Modular Design:*

  * main.py → orchestrates test execution
  * avi_api_utils.py → handles API logic and helper methods
* *4-Stage Workflow:* Pre-Fetcher → Pre-Validation → Task/Trigger → Post-Validation
* *Mocks:* Includes stubbed SSH and RDP methods.

---

## Setup

1. *Clone Repo*

   bash
   git clone https://github.com/Hemnath0/Python-Test-Automation-Framework.git
   cd Python-Test-Automation-Framework
   
2. *Install Dependencies*

   bash
   pip install -r requirements.txt
   
3. *Update Token*
   Edit config.yaml and replace the placeholder token with your active session token:

   yaml
   api:
     token: "your-token-here"
     headers:
       Authorization: "Bearer your-token-here"
   

---

## Jenkins CI/CD Pipeline Integration

### Jenkins Setup

Run Jenkins in Docker with root privileges:

bash
docker run -d --name jenkins_server \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --user root jenkins/jenkins:lts-jdk11


Then open [http://localhost:8080](http://localhost:8080), unlock Jenkins, install suggested plugins, and create an admin user.

### Required Plugins

* *Pipeline*
* *Git Plugin*

### Pipeline Overview (Jenkinsfile)

| Stage                                  | Description                                                             |
| -------------------------------------- | ----------------------------------------------------------------------- |
| *Checkout*                           | Pulls source code from Git.                                             |
| *Setup Environment & Run Automation* | Creates Python venv, installs dependencies, and executes the framework. |

### Build Triggers

* *Manual:* “Build Now”
* *Scheduled:* Hourly (H * * * *)

---
