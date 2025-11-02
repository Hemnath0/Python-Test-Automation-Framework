// Jenkinsfile (THE TRUE FINAL VERSION)

pipeline {
    // CRITICAL: We revert to 'agent any' and rely entirely on the 'script' block later.
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON_EXEC = "venv/bin/python" // Note: This path is relative to the workspace, now guaranteed by the Docker execution
        PIP_EXEC = "venv/bin/pip"
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

        // CRITICAL FIX: Wrap all scripted docker logic inside a 'script' block
        stage('Execute Automation') {
            steps {
                script { // <---- THIS IS THE FIX: Opens the Groovy Scripting Context
                    docker.image('python:3.9-slim').inside {
                        sh '''
                            echo "Running stages inside python:3.9-slim container..."
                            
                            # --- Stage: Setup Environment ---
                            echo "Creating and installing Python virtual environment..."
                            
                            # Use system python in the container to create venv
                            python -m venv ${VENV_DIR}
                            
                            # Installation using venv's pip executable
                            ${PIP_EXEC} install --no-cache-dir -r requirements.txt
                            echo "Environment setup complete. Python version used:"
                            ${PYTHON_EXEC} --version

                            # --- Stage: Run Automation ---
                            echo "Starting automation framework execution..."
                            
                            # Execute the main script
                            ${PYTHON_EXEC} main.py --config config.yml
                            echo "Automation execution finished successfully."
                        '''
                    }
                } // <---- End of script block
            }
        }
    }
    
    // Cleanup must be in the outer Declarative context
    post {
        always {
             // Cleanup: Remove the virtual environment
             sh 'rm -rf venv'
             echo "Workspace cleanup complete: removed venv"
        }
    }
}