// Jenkinsfile

pipeline {
    // Defines where the pipeline runs. 'any' uses any available executor on the Jenkins node.
    agent any
    
    // Environment variables are defined here, making paths reusable.
    environment {
        // Defines the name of the Python virtual environment folder.
        VENV_DIR = 'venv' 
        // Defines the executable path for the Python interpreter inside the venv.
        // We use $VENV_DIR/bin/python for consistency in Linux-based environments (like Jenkins/Docker).
        PYTHON_EXEC = "${VENV_DIR}/bin/python" 
    }
    
    // Global options for the pipeline.
    options {
        // Adds timestamps to the console output for better readability.
        timestamps()
    }

    stages {
        
        // Stage 1: Checkout (Fetching the Code)
        stage('Checkout') {
            steps {
                // The Git checkout process is handled automatically by the job configuration itself,
                // but this echo provides a clear visual confirmation in the pipeline log.
                echo 'Source code pulled from Git repository.'
            }
        }

        // Stage 2: Setup Environment
        stage('Setup Environment') {
            steps {
                // The 'sh' step executes shell commands.
                sh '''
                    echo "Creating and activating Python virtual environment..."
                    # 1. Create the virtual environment
                    python3 -m venv ${VENV_DIR}
                    
                    # 2. Activate the virtual environment and install dependencies
                    # This uses bash source command which is standard in Linux
                    source ${VENV_DIR}/bin/activate
                    
                    # 3. Install dependencies from requirements.txt
                    pip install --no-cache-dir -r requirements.txt
                    
                    echo "Environment setup complete. Python version:"
                    ${PYTHON_EXEC} --version
                '''
            }
        }

        // Stage 3: Run Automation
        stage('Run Automation') {
            steps {
                // Ensure the script is executed using the interpreter inside the virtual environment.
                // The pipeline will FAIL if 'python main.py' exits with a non-zero code (e.g., test failure).
                sh """
                    echo "Starting automation framework execution..."
                    
                    # 1. Run the main script using the virtual environment's Python
                    # Note: We don't need 'source activate' here if we use the full path to the executable.
                    ${PYTHON_EXEC} main.py --config config.yml
                    
                    echo "Automation execution finished successfully."
                """
            }
        }
    }
    
    // Post-build actions for cleanup and reporting
    post {
        // Runs only if the overall pipeline failed.
        failure {
            echo 'Pipeline failed! Review "Run Automation" console output for errors.'
        }
        // Always runs at the end, regardless of success or failure.
        always {
             // Cleanup: Remove the virtual environment to keep the workspace tidy.
             sh 'rm -rf ${VENV_DIR}'
             echo "Workspace cleanup complete: removed ${VENV_DIR}"
        }
    }
}