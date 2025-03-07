pipeline {
    agent any

    environment {
        IMAGE_NAME = "your-dockerhub-username/your-app"
        IMAGE_TAG = "latest"
        DOCKER_HUB_CREDENTIALS = "docker-hub-credentials"
        ADMIN_EMAIL = "admin@example.com"  // Change to your admin email
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'master', url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "Deployment successful. Sending email notification..."

            emailext (
                to: "${ADMIN_EMAIL}",
                subject: "Deployment Successful: ${IMAGE_NAME}:${IMAGE_TAG}",
                body: """
                The deployment of the application was successful.

                - Repository: https://github.com/your-username/your-repo
                - Deployed Image: ${IMAGE_NAME}:${IMAGE_TAG}
                - Deployment Time: ${new Date()}
                
                Jenkins Job: ${env.BUILD_URL}
                """,
                attachLog: true
            )
        }
        failure {
            echo "Deployment failed. Sending failure notification..."

            emailext (
                to: "${ADMIN_EMAIL}",
                subject: "Deployment Failed: ${IMAGE_NAME}:${IMAGE_TAG}",
                body: """
                The deployment of the application has failed.

                - Repository: https://github.com/your-username/your-repo
                - Attempted Image: ${IMAGE_NAME}:${IMAGE_TAG}
                - Failure Time: ${new Date()}
                
                Jenkins Job: ${env.BUILD_URL}

                Please check the Jenkins logs for more details.
                """,
                attachLog: true
            )
        }
    }
}
