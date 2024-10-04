pipeline {
    agent any
    stages {
        stage('Docker Login') {
            steps {
                // Log in to Docker Hub using Jenkins credentials.
                withCredentials([usernamePassword(credentialsId: 'dockerhub-idps-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build the Docker image locally on the Jenkins server and tag it as 'damdda-ai-flask-server'.
                sh 'docker build -t docker.io/pmhchris/damdda-ai-flask-server .'
                
                // Push the Docker image to Docker Hub.
                sh 'docker push docker.io/pmhchris/damdda-ai-flask-server'
            }
        }
        stage('Deploy to Remote Server') {
            steps {
                // SSH into the remote server and run Docker commands.
                sshagent (credentials: ['jenkins-ssh-credentials']) {
                    sh '''
                        ssh user@211.188.48.96 << EOF
                            # Stop the running container if it exists.
                            docker stop damdda-ai-flask-server || true
                            # Remove the existing container.
                            docker rm damdda-ai-flask-server || true
                            
                            # Pull the latest Docker image from Docker Hub.
                            docker pull docker.io/pmhchris/damdda-ai-flask-server
                            
                            # Run a new container from the pulled image, exposing it on port 5000.
                            docker run -d --name damdda-ai-flask-server -p 5000:5000 docker.io/pmhchris/damdda-ai-flask-server
                        EOF
                    '''
                }
            }
        }
    }
}
