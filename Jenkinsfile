pipeline {
    agent any
    stages {
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-idps-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    // Log in to Docker Hub locally
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t docker.io/pmhchris/damdda-ai-flask-server:latest .'
                
                // Push the Docker image to Docker Hub
                sh 'docker push docker.io/pmhchris/damdda-ai-flask-server:latest'
            }
        }
        stage('Deploy to Remote Server') {
            steps {
                sshagent (credentials: ['jenkins-ssh-credentials']) {
                    sh '''
                        ssh damdda@211.188.48.96 << EOF
                            # Log the Docker username for verification
                            echo "DOCKER_USERNAME is: $DOCKER_USERNAME"
                            
                            # Log in to Docker Hub using environment variables
                            export DOCKER_USERNAME='${DOCKER_USERNAME}'
                            export DOCKER_PASSWORD='${DOCKER_PASSWORD}'
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                            
                            # Stop the running container if it exists
                            docker stop damdda-ai-flask-server || true
                            # Remove the existing container
                            docker rm damdda-ai-flask-server || true
                            
                            # Pull the latest image from Docker Hub
                            docker pull docker.io/pmhchris/damdda-ai-flask-server:latest
                            
                            # Run a new container from the pulled image
                            docker run -d --name damdda-ai-flask-server -p 5000:5000 docker.io/pmhchris/damdda-ai-flask-server:latest
                        EOF
                    '''
                }
            }
        }
    }
}
