// Jenkinsfile (FINAL VERSION with Installation Fix)

pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv' 
        // We set up the executable paths based on the expected location after VENV creation.
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

        // Stage 2: Setup Environment (CRITICAL FIX IMPLEMENTED HERE)
        stage('Setup Environment') {
            steps {
                sh '''
                    echo "Ensuring Python Venv tools are installed..."
                    
                    # --- FIX START ---
                    # 1. Update package list and install the python3-venv package
                    # This guarantees the 'python3' command and 'venv' module are available.
                    apt-get update
                    apt-get install -y python3-venv
                    # --- FIX END ---
                    
                    echo "Creating and installing Python virtual environment..."
                    
                    # 2. Create the virtual environment using 'python3' (guaranteed to be found now)
                    python3 -m venv ${VENV_DIR}
                    
                    # 3. Use the venv's specific pip executable to install dependencies.
                    ${PIP_EXEC} install --no-cache-dir -r requirements.txt
                    
                    echo "Environment setup complete. Python version used:"
                    ${PYTHON_EXEC} --version
                '''
            }
        }

        // Stage 3: Run Automation
        stage('Run Automation') {
            steps {
                sh """
                    echo "Starting automation framework execution..."
                    
                    # Execute the main script using the virtual environment's Python interpreter.
                    ${PYTHON_EXEC} main.py --config config.yml
                    
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
             // Cleanup: Remove the virtual environment to keep the workspace tidy.
             sh 'rm -rf ${VENV_DIR}'
             echo "Workspace cleanup complete: removed ${VENV_DIR}"
        }
    }
}