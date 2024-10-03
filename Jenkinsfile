pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                // Build the Docker image and tag it as 'damdda-ai-flask-server'.
                sh 'docker build -t damdda-ai-flask-server .'
            }
        }
        stage('Run Docker Container') {
            steps {
                // Stop and remove the existing container if it's running
                sh 'docker stop damdda-ai-flask-server || true && docker rm damdda-ai-flask-server || true'
                // Run a new container from the built image, exposing it on port 5000
                sh 'docker run -d --name damdda-ai-flask-server -p 5000:5000 damdda-ai-flask-server'
            }
        }
    }
}
