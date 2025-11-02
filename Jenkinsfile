// Jenkinsfile (ABSOLUTELY FINAL VERSION)

pipeline {
    // We use 'agent any' to ensure the Jenkins Controller can start the job.
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_EXEC = "/usr/local/bin/python" 
        PIP_EXEC = "/usr/local/bin/pip"
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

        // CRITICAL FIX: Run the rest of the pipeline inside a guaranteed Python container
        stage('Execute Automation') {
            steps {
                // Use a script block to execute multiple shell steps inside a Docker image.
                // This bypasses the Jenkins controller's 'docker not found' error.
                docker.image('python:3.9-slim').inside {
                    sh '''
                        echo "Running stages inside python:3.9-slim container..."
                        
                        # --- Stage: Setup Environment ---
                        echo "Creating and installing Python virtual environment..."
                        # Venv creation: Python is guaranteed to be available here
                        python -m venv ${VENV_DIR}
                        
                        # Installation
                        ${VENV_DIR}/bin/pip install --no-cache-dir -r requirements.txt
                        echo "Environment setup complete. Python version used:"
                        ${VENV_DIR}/bin/python --version

                        # --- Stage: Run Automation ---
                        echo "Starting automation framework execution..."
                        # Execute the main script
                        ${VENV_DIR}/bin/python main.py --config config.yml
                        echo "Automation execution finished successfully."
                    '''
                }
            }
        }
    }
    
    // Cleanup must be outside the docker.image block
    post {
        failure {
            echo 'Pipeline failed! Review the console output for the "Execute Automation" stage.'
        }
        always {
             // Cleanup: Remove the virtual environment from the workspace BEFORE the next build.
             // This runs on the Jenkins Controller (agent any context)
             sh 'rm -rf venv'
             echo "Workspace cleanup complete: removed venv"
        }
    }
}