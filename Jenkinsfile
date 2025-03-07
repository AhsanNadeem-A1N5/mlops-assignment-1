pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "AhsanNadeem-A1N5/MLOPS-Assignment1"
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/AhsanNadeem-A1N5/mlops-assignment-1.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u your-dockerhub-username --password-stdin'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh 'docker rmi $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }
    }

    post {
        success {
            emailext subject: "Docker Image Uploaded Successfully",
                     body: "The Docker image $DOCKER_IMAGE:$DOCKER_TAG has been successfully pushed to Docker Hub.",
                     to: "ahsannadeem00321@gmail.com",
                     from: "jenkins@example.com"
        }
        failure {
            emailext subject: "Docker Build Failed",
                     body: "The Jenkins pipeline for Docker image build and push has failed.",
                     to: "ahsannadeem00321@gmail.com",
                     from: "jenkins@example.com"
        }
    }
}
