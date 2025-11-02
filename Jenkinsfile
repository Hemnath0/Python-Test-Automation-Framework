// Jenkinsfile

pipeline {
    // Defines where the pipeline runs. 'any' uses any available executor on the Jenkins node.
    agent any
    
    // Environment variables are defined here, making paths reusable.
    environment {
        // Defines the name of the Python virtual environment folder.
        VENV_DIR = 'venv' 
        // Defines the executable path for the Python interpreter inside the venv (Standard Linux path).
        PYTHON_EXEC = "${VENV_DIR}/bin/python" 
        // Defines the executable path for pip inside the venv (Standard Linux path).
        PIP_EXEC = "${VENV_DIR}/bin/pip"
    }
    
    // Global options for the pipeline.
    options {
        // Adds timestamps to the console output for better readability.
        timestamps()
    }

    stages {
        
        // Stage 1: Checkout
        stage('Checkout') {
            steps {
                // SCM is handled by job configuration. This provides a visual log entry.
                echo 'Source code pulled from Git repository.'
            }
        }

        // Stage 2: Setup Environment (Creation, Activation, and Dependency Install)
        stage('Setup Environment') {
            steps {
                // The 'sh' step executes shell (Linux) commands inside the Jenkins container.
                sh '''
                    echo "Creating and installing Python virtual environment..."
                    
                    # 1. Create the virtual environment using 'python' command (the fix for 'python3: not found')
                    python -m venv ${VENV_DIR}
                    
                    # 2. Install dependencies using the venv's specific pip executable
                    ${PIP_EXEC} install --no-cache-dir -r requirements.txt
                    
                    echo "Environment setup complete. Python version used:"
                    ${PYTHON_EXEC} --version
                '''
            }
        }

        // Stage 3: Run Automation
        stage('Run Automation') {
            steps {
                // Execute the main script using the virtual environment's Python interpreter.
                // The pipeline will FAIL if the script exits with a non-zero code (e.g., test failure).
                sh """
                    echo "Starting automation framework execution..."
                    
                    ${PYTHON_EXEC} main.py --config config.yml
                    
                    echo "Automation execution finished successfully."
                """
            }
        }
    }
    
    // Post-build actions for cleanup and reporting
    post {
        // Runs if the overall pipeline failed.
        failure {
            echo 'Pipeline failed! Review the console output for the "Run Automation" stage.'
        }
        // Always runs at the end, regardless of success or failure.
        always {
             // Cleanup: Remove the virtual environment to keep the workspace tidy.
             sh 'rm -rf ${VENV_DIR}'
             echo "Workspace cleanup complete: removed ${VENV_DIR}"
        }
    }
}