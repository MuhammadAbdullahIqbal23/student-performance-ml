pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'student-performance-ml'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_LATEST = 'latest'
        DOCKERHUB_CREDENTIALS = credentials('muhammadabdullahiqbal-dockerhub')
        EMAIL_RECIPIENTS = credentials('lifedbs20@gmail.com,abdulahiqbal1133@gmail.com')
    }
    
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'master', description: 'Git branch name')
        string(name: 'COMMIT_SHA', defaultValue: '', description: 'Git commit SHA')
        string(name: 'COMMIT_MESSAGE', defaultValue: '', description: 'Git commit message')
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 20, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Building from branch: ${params.BRANCH_NAME}"
                    echo "Commit SHA: ${params.COMMIT_SHA}"
                    echo "Commit Message: ${params.COMMIT_MESSAGE}"
                }
                
                checkout scm
                
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    env.IMAGE_NAME = "${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}"
                    env.IMAGE_TAG_BUILD = "${env.IMAGE_NAME}:${DOCKER_TAG}"
                    env.IMAGE_TAG_LATEST = "${env.IMAGE_NAME}:${DOCKER_LATEST}"
                    env.IMAGE_TAG_COMMIT = "${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                }
                
                echo "Docker Image: ${env.IMAGE_NAME}"
                echo "Build Tag: ${env.IMAGE_TAG_BUILD}"
                echo "Latest Tag: ${env.IMAGE_TAG_LATEST}"
                echo "Commit Tag: ${env.IMAGE_TAG_COMMIT}"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    
                    // Build the Docker image
                    def image = docker.build("${env.IMAGE_NAME}:${DOCKER_TAG}")
                    
                    // Tag the image with multiple tags
                    sh """
                        docker tag ${env.IMAGE_TAG_BUILD} ${env.IMAGE_TAG_LATEST}
                        docker tag ${env.IMAGE_TAG_BUILD} ${env.IMAGE_TAG_COMMIT}
                    """
                    
                    echo "✅ Docker image built successfully"
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                script {
                    echo "Testing Docker image..."
                    
                    // Run a quick test to ensure the image works
                    sh """
                        docker run --rm -d --name test-container-${BUILD_NUMBER} -p 5001:5000 ${env.IMAGE_TAG_BUILD}
                        sleep 10
                        
                        # Test health endpoint
                        curl -f http://localhost:5001/health || (docker logs test-container-${BUILD_NUMBER} && exit 1)
                        
                        # Stop test container
                        docker stop test-container-${BUILD_NUMBER} || true
                    """
                    
                    echo "✅ Docker image test passed"
                }
            }
            post {
                always {
                    sh "docker stop test-container-${BUILD_NUMBER} || true"
                    sh "docker rm test-container-${BUILD_NUMBER} || true"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        // Push all tags
                        sh """
                            docker push ${env.IMAGE_TAG_BUILD}
                            docker push ${env.IMAGE_TAG_LATEST}
                            docker push ${env.IMAGE_TAG_COMMIT}
                        """
                    }
                    
                    echo "✅ Docker image pushed successfully to Docker Hub"
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning up local Docker images..."
                    
                    sh """
                        docker rmi ${env.IMAGE_TAG_BUILD} || true
                        docker rmi ${env.IMAGE_TAG_LATEST} || true
                        docker rmi ${env.IMAGE_TAG_COMMIT} || true
                        docker system prune -f
                    """
                    
                    echo "✅ Cleanup completed"
                }
            }
        }
    }
    
    post {
        success {
            script {
                def buildDuration = currentBuild.durationString.replace(' and counting', '')
                def emailBody = """
                <html>
                <body>
                    <h2>🎉 Jenkins Build Successful</h2>
                    <p><strong>Project:</strong> Student Performance ML</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Branch:</strong> ${params.BRANCH_NAME}</p>
                    <p><strong>Commit:</strong> ${params.COMMIT_SHA}</p>
                    <p><strong>Commit Message:</strong> ${params.COMMIT_MESSAGE}</p>
                    <p><strong>Build Duration:</strong> ${buildDuration}</p>
                    <p><strong>Docker Images Published:</strong></p>
                    <ul>
                        <li>${env.IMAGE_TAG_BUILD}</li>
                        <li>${env.IMAGE_TAG_LATEST}</li>
                        <li>${env.IMAGE_TAG_COMMIT}</li>
                    </ul>
                    <p><strong>Jenkins Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Docker Hub Repository:</strong> <a href="https://hub.docker.com/r/${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}">View on Docker Hub</a></p>
                    <hr>
                    <p><em>This is an automated notification from Jenkins CI/CD Pipeline</em></p>
                </body>
                </html>
                """
                
                emailext (
                    subject: "✅ Jenkins Build #${BUILD_NUMBER} - SUCCESS - Student Performance ML",
                    body: emailBody,
                    mimeType: 'text/html',
                    to: "${EMAIL_RECIPIENTS}",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ]
                )
                
                echo "✅ Success notification email sent to administrators"
            }
        }
        
        failure {
            script {
                def buildDuration = currentBuild.durationString.replace(' and counting', '')
                def emailBody = """
                <html>
                <body>
                    <h2>❌ Jenkins Build Failed</h2>
                    <p><strong>Project:</strong> Student Performance ML</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Branch:</strong> ${params.BRANCH_NAME}</p>
                    <p><strong>Commit:</strong> ${params.COMMIT_SHA}</p>
                    <p><strong>Commit Message:</strong> ${params.COMMIT_MESSAGE}</p>
                    <p><strong>Build Duration:</strong> ${buildDuration}</p>
                    <p><strong>Failed Stage:</strong> ${env.STAGE_NAME ?: 'Unknown'}</p>
                    <p><strong>Jenkins Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Console Output:</strong> <a href="${BUILD_URL}console">View Console Log</a></p>
                    <hr>
                    <p style="color: red;"><strong>Immediate attention required!</strong></p>
                    <p><em>This is an automated notification from Jenkins CI/CD Pipeline</em></p>
                </body>
                </html>
                """
                
                emailext (
                    subject: "❌ Jenkins Build #${BUILD_NUMBER} - FAILED - Student Performance ML",
                    body: emailBody,
                    mimeType: 'text/html',
                    to: "${EMAIL_RECIPIENTS}",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ]
                )
                
                echo "❌ Failure notification email sent to administrators"
            }
        }
        
        unstable {
            script {
                emailext (
                    subject: "⚠️ Jenkins Build #${BUILD_NUMBER} - UNSTABLE - Student Performance ML",
                    body: """Build completed with warnings. Please check the console output: ${BUILD_URL}console""",
                    to: "${EMAIL_RECIPIENTS}"
                )
            }
        }
        
        always {
            // Archive build artifacts if any
            script {
                if (fileExists('build-info.txt')) {
                    archiveArtifacts artifacts: 'build-info.txt', fingerprint: true
                }
            }
            
            // Clean workspace
            cleanWs(
                deleteDirs: true,
                notFailBuild: true,
                patterns: [[pattern: '.git', type: 'EXCLUDE']]
            )
        }
    }
}