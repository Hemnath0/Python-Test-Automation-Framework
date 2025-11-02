// Jenkinsfile (NATIVE PYTHON FIX)

pipeline {
    // Run directly on the Jenkins controller (which is now running as root)
    agent any 

    environment {
        VENV_DIR = 'venv' 
        PYTHON_EXEC = "${VENV_DIR}/bin/python" 
        PIP_EXEC = "${VENV_DIR}/bin/pip"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code pulled from Git repository.'
            }
        }

        // This stage MUST execute cleanly now because the container is running as root
        stage('Setup Environment & Run Automation') {
            steps {
                sh '''
                    echo "--- Stage: Setup Environment ---"

                    # 1. FIX: Update package list and install the python3-venv package (Requires root, which we fixed)
                    apt-get update
                    apt-get install -y python3-venv

                    # 2. Create the virtual environment
                    python3 -m venv ${VENV_DIR}

                    # 3. Install dependencies
                    ${PIP_EXEC} install --no-cache-dir -r requirements.txt
                    echo "Environment setup complete. Python version used:"
                    ${PYTHON_EXEC} --version

                    echo "--- Stage: Run Automation ---"

                    # 4. Execute the main script
                    ${PYTHON_EXEC} main.py --config config.yml
                    echo "Automation execution finished successfully."
                '''
            }
        }
    }

    post {
        always {
             sh 'rm -rf venv'
             echo "Workspace cleanup complete: removed venv"
        }
    }
}