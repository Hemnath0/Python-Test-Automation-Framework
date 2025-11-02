// Jenkinsfile (FINAL PRODUCTION-READY VERSION)

pipeline {
    // CRITICAL FIX: Use a Docker agent that already has Python 3 and venv installed.
    // This isolates the build and removes the need for 'apt-get install'.
    agent {
        docker {
            image 'python:3.9-slim' // Official Python image with everything we need
            // Ensure the workspace is mounted inside the container
            args '-u root:root' // Run as root to prevent any file permission issues
        }
    }
    
    // Environment variables are now implicitly available inside the Python container
    environment {
        VENV_DIR = 'venv' 
        // Python executables are in standard /usr/local/bin inside the python:3.9-slim image
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

        // Stage 2: Setup Environment (CLEANED UP - No more apt-get needed!)
        stage('Setup Environment') {
            steps {
                sh '''
                    echo "Creating and installing Python virtual environment..."
                    
                    # 1. We no longer need 'apt-get' since the image is 'python:3.9-slim'
                    
                    # 2. Create the virtual environment (uses the PYTHON_EXEC in the container)
                    ${PYTHON_EXEC} -m venv ${VENV_DIR}
                    
                    # 3. Use the venv's specific pip executable to install dependencies.
                    # Note: Inside the python container, the system pip is already available, 
                    # but using the venv is still best practice for dependency isolation.
                    ${VENV_DIR}/bin/pip install --no-cache-dir -r requirements.txt
                    
                    echo "Environment setup complete. Python version used:"
                    ${VENV_DIR}/bin/python --version
                '''
            }
        }

        // Stage 3: Run Automation
        stage('Run Automation') {
            steps {
                sh """
                    echo "Starting automation framework execution..."
                    
                    # Execute the main script using the virtual environment's Python interpreter.
                    ${VENV_DIR}/bin/python main.py --config config.yml
                    
                    echo "Automation execution finished successfully."
                """
            }
        }
    }
    
    post {
        failure {
            echo 'Pipeline failed! Review the console output for the "Run Automation" stage.'
        }
        always {
             // Cleanup: The temporary 'venv' is removed.
             sh 'rm -rf ${VENV_DIR}'
             echo "Workspace cleanup complete: removed ${VENV_DIR}"
        }
    }
}