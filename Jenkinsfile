pipeline {
    agent any
    stages {
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-idps-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    // Authenticate with Docker Hub using credentials stored in Jenkins
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build the Docker image with the latest version
                sh 'docker build -t docker.io/pmhchris/damdda-ai-flask-server:latest .'
                
                // Push the Docker image to Docker Hub
                sh 'docker push docker.io/pmhchris/damdda-ai-flask-server:latest'
            }
        }
        stage('Deploy to Remote Server') {
            steps {
                sshagent (credentials: ['jenkins-ssh-credentials']) {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-idps-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh """
                            ssh damdda@211.188.48.96 << 'EOF'
echo '${DOCKER_PASSWORD}' | docker login -u '${DOCKER_USERNAME}' --password-stdin

docker stop damdda-ai-flask-server || true
docker rm damdda-ai-flask-server || true

docker pull docker.io/pmhchris/damdda-ai-flask-server:latest

docker run -d --name damdda-ai-flask-server -p 5000:5000 docker.io/pmhchris/damdda-ai-flask-server:latest
EOF
                        """
                    }
                }
            }
        }
    }
}
