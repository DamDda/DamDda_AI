pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                // GitHub에서 레포지토리 클론
                git 'https://github.com/DamDda/DamDda_AI.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                // Docker 이미지를 빌드하고 'damdda-ai-flask-server'로 태그
                sh 'docker build -t damdda-ai-flask-server .'
            }
        }
        stage('Run Docker Container') {
            steps {
                // 기존 실행 중인 컨테이너가 있으면 중지하고 제거
                sh 'docker stop damdda-ai-flask-server || true && docker rm damdda-ai-flask-server || true'
                // 새로 빌드한 이미지를 사용해 5000번 포트로 컨테이너 실행
                sh 'docker run -d --name damdda-ai-flask-server -p 5000:5000 damdda-ai-flask-server'
            }
        }
    }
}
