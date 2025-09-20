pipeline {
    agent any
    
    parameters {
        string(name: 'DOCKER_IMAGE_TAG', defaultValue: '1', description: 'Docker image tag from GitHub Actions')
        string(name: 'GIT_COMMIT', defaultValue: '', description: 'Git commit SHA')
        string(name: 'GIT_BRANCH', defaultValue: 'master', description: 'Git branch name')
        string(name: 'BUILD_NUMBER', defaultValue: '1', description: 'GitHub Actions build number')
        string(name: 'REPOSITORY_URL', defaultValue: '', description: 'GitHub repository URL')
    }
    
    environment {
        DOCKER_IMAGE = 'student-performance-ml'
        DOCKER_REGISTRY = 'docker.io'
    }
    
    stages {
        stage('Initialize') {
            steps {
                script {
                    // Set display name for better identification
                    currentBuild.displayName = "#${env.BUILD_NUMBER} - Tag: ${params.DOCKER_IMAGE_TAG}"
                    currentBuild.description = "Deploy ${params.GIT_COMMIT?.take(8)} from ${params.GIT_BRANCH}"
                }
                
                echo "🚀 Starting Jenkins deployment pipeline"
                echo "Docker Image Tag: ${params.DOCKER_IMAGE_TAG}"
                echo "Git Commit: ${params.GIT_COMMIT}"
                echo "Git Branch: ${params.GIT_BRANCH}"
                echo "Repository: ${params.REPOSITORY_URL}"
            }
        }
        
        stage('Docker Environment Check') {
            steps {
                script {
                    echo "🔧 Checking Docker availability on agent"
                    // We'll detect docker and set an environment flag so later stages can decide what to do
                    try {
                        sh 'docker --version'
                        // if docker command exists, try docker info to ensure daemon is reachable
                        try {
                            sh 'docker info'
                            echo "✅ Docker is available on this agent"
                            env.DOCKER_AVAILABLE = 'true'
                        } catch (Exception exInfo) {
                            echo "⚠️ Docker CLI present but daemon not reachable: ${exInfo.getMessage()}"
                            env.DOCKER_AVAILABLE = 'false'
                        }
                    } catch (Exception e) {
                        echo "⚠️ Docker CLI not found on this agent: ${e.getMessage()}"
                        env.DOCKER_AVAILABLE = 'false'
                    }
                }
            }
        }
        
        stage('Verify Docker Image') {
            steps {
                script {
                    echo "🔍 Verifying Docker image availability"
                    
                    // Check if Docker Hub credentials exist and verify image.
                    // If Docker is available we'll use the docker client; otherwise fall back to Docker Hub HTTP API.
                    withCredentials([usernamePassword(credentialsId: '6bfeb15d-259a-4042-8042-0b064c643e50', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        def imageName = "${DOCKER_USER}/${DOCKER_IMAGE}:${params.DOCKER_IMAGE_TAG}"
                        if (env.DOCKER_AVAILABLE == 'true') {
                            echo "🔐 Docker available: using docker client to verify image"
                            try {
                                sh '''
                                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                                '''
                                sh """
                                    docker pull ${imageName}
                                    docker inspect ${imageName}
                                """
                                echo "✅ Docker image verified successfully with docker client"
                            } catch (Exception e) {
                                error "❌ Failed to verify Docker image with docker client: ${e.getMessage()}"
                            }
                        } else {
                            echo "� Docker not available: using Docker Hub API to verify image manifest"
                            try {
                                // Get an access token from Docker Hub
                                def tokenCmd = "curl -s -u ${DOCKER_USER}:${DOCKER_PASS} \"https://auth.docker.io/token?service=registry.docker.io&scope=repository:${DOCKER_USER}/${DOCKER_IMAGE}:pull\" | sed -n 's/.*\\\"token\\\":\\\"\\\([^\\\"]*\\\)\\\".*/\\1/p'"
                                def token = sh(script: tokenCmd, returnStdout: true).trim()
                                if (!token) {
                                    error "❌ Failed to obtain token from Docker Hub (empty token)"
                                }

                                def manifestUrl = "https://registry-1.docker.io/v2/${DOCKER_USER}/${DOCKER_IMAGE}/manifests/${params.DOCKER_IMAGE_TAG}"
                                def statusCmd = "curl -s -o /dev/null -w \"%{http_code}\" -H 'Authorization: Bearer ${token}' -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' ${manifestUrl}"
                                def status = sh(script: statusCmd, returnStdout: true).trim()
                                if (status == '200') {
                                    echo "✅ Docker image manifest exists on Docker Hub (status ${status})"
                                } else {
                                    error "❌ Manifest check failed (HTTP ${status}) for ${imageName}"
                                }
                            } catch (Exception e) {
                                error "❌ Failed to verify Docker image via Docker Hub API: ${e.getMessage()}"
                            }
                        }
                    }
                }
            }
        }
        
        stage('Test Container') {
            steps {
                script {
                    echo "🧪 Testing containerized application"
                    
                    // If Docker isn't available on the agent, skip runtime container tests
                    if (env.DOCKER_AVAILABLE == 'true') {
                        withCredentials([usernamePassword(credentialsId: '6bfeb15d-259a-4042-8042-0b064c643e50', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            def imageName = "${DOCKER_USER}/${DOCKER_IMAGE}:${params.DOCKER_IMAGE_TAG}"
                            def containerName = "test-${DOCKER_IMAGE}-${env.BUILD_NUMBER}"
                            
                            try {
                                // Run container for testing
                                sh """
                                    docker run -d --name ${containerName} -p 5001:5000 ${imageName}
                                    sleep 15
                                """
                                
                                // Test health endpoint
                                sh """
                                    curl -f http://localhost:5001/health || exit 1
                                    echo "✅ Health check passed"
                                """
                                
                                // Test prediction endpoint with sample data
                                sh """
                                    curl -X POST -H 'Content-Type: application/json' \
                                        -d '{"age": 18, "gender": "Female", "previous_gpa": 3.5, "study_hours_per_week": 20, "attendance_rate": 85, "parental_education": "Bachelor", "household_income": 50000, "class_size": 25, "has_internet": 1, "has_computer": 1, "school_type": "Public", "sleep_hours": 7, "exercise_hours_per_week": 3, "extracurricular_hours": 5}' \
                                        http://localhost:5001/predict || exit 1
                                    echo "✅ Prediction endpoint test passed"
                                """
                                
                                echo "✅ Container testing completed successfully"
                                
                            } catch (Exception e) {
                                error "❌ Container testing failed: ${e.getMessage()}"
                            } finally {
                                // Cleanup test container
                                sh """
                                    docker stop ${containerName} || true
                                    docker rm ${containerName} || true
                                """
                            }
                        }
                    } else {
                        echo "⚠️ Skipping container runtime tests because Docker is not available on this agent"
                    }
                }
            }
        }
        
        stage('Tag and Push Final Image') {
            steps {
                script {
                    echo "🏷️ Tagging and pushing final production image"
                    
                    if (env.DOCKER_AVAILABLE == 'true') {
                        withCredentials([usernamePassword(credentialsId: '6bfeb15d-259a-4042-8042-0b064c643e50', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            def sourceImage = "${DOCKER_USER}/${DOCKER_IMAGE}:${params.DOCKER_IMAGE_TAG}"
                            def prodImage = "${DOCKER_USER}/${DOCKER_IMAGE}:production"
                            def stableImage = "${DOCKER_USER}/${DOCKER_IMAGE}:stable"
                            
                            try {
                                // Login to Docker Hub for pushing
                                sh '''
                                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                                '''
                                
                                // Tag as production and stable
                                sh """
                                    docker tag ${sourceImage} ${prodImage}
                                    docker tag ${sourceImage} ${stableImage}
                                    
                                    docker push ${prodImage}
                                    docker push ${stableImage}
                                """
                                
                                echo "✅ Production images pushed successfully"
                                
                            } catch (Exception e) {
                                error "❌ Failed to tag and push production image: ${e.getMessage()}"
                            }
                        }
                    } else {
                        echo "⚠️ Skipping image tagging/pushing because Docker is not available on this agent"
                    }
                }
            }
        }
        
        stage('Deployment Verification') {
            steps {
                script {
                    echo "✅ Deployment verification completed"
                    echo "📦 Available Docker Images:"
                    
                    try {
                        withCredentials([usernamePassword(credentialsId: '6bfeb15d-259a-4042-8042-0b064c643e50', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            echo "  - ${DOCKER_USER}/${DOCKER_IMAGE}:${params.DOCKER_IMAGE_TAG}"
                            echo "  - ${DOCKER_USER}/${DOCKER_IMAGE}:production"
                            echo "  - ${DOCKER_USER}/${DOCKER_IMAGE}:stable"
                            echo "  - ${DOCKER_USER}/${DOCKER_IMAGE}:latest"
                        }
                    } catch (Exception e) {
                        echo "  - Docker images deployed (credentials not available for display)"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Cleanup Docker images to save space (only if Docker is available)
                try {
                    sh 'docker system prune -f'
                    echo "✅ Docker cleanup completed"
                } catch (Exception e) {
                    echo "⚠️ Docker cleanup skipped - Docker not available: ${e.getMessage()}"
                }
            }
        }
        
        success {
            script {
                echo "🎉 Jenkins pipeline completed successfully!"
                
                // Check if email credentials exist before sending
                try {
                    def emailList = env.NOTIFICATION_EMAIL ?: 'abdullahiqbal1133@gmail.com'
                    
                    // Send success email notification
                    emailext (
                        subject: "✅ Deployment Successful - Student Performance ML [Build #${env.BUILD_NUMBER}]",
                        body: """
                        <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2 style="color: #28a745;">🎉 Deployment Completed Successfully!</h2>
                            
                            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>📋 Build Information</h3>
                                <ul>
                                    <li><strong>Project:</strong> Student Performance ML</li>
                                    <li><strong>Jenkins Build:</strong> #${env.BUILD_NUMBER}</li>
                                    <li><strong>GitHub Build:</strong> #${params.BUILD_NUMBER}</li>
                                    <li><strong>Git Commit:</strong> <code>${params.GIT_COMMIT}</code></li>
                                    <li><strong>Branch:</strong> ${params.GIT_BRANCH}</li>
                                    <li><strong>Repository:</strong> <a href="${params.REPOSITORY_URL}">${params.REPOSITORY_URL}</a></li>
                                    <li><strong>Build Time:</strong> ${new Date()}</li>
                                </ul>
                            </div>
                            
                            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>🐳 Docker Images</h3>
                                <ul>
                                    <li><code>${env.DOCKERHUB_CREDENTIALS_USR ?: 'username'}/${DOCKER_IMAGE}:${params.DOCKER_IMAGE_TAG}</code></li>
                                    <li><code>${env.DOCKERHUB_CREDENTIALS_USR ?: 'username'}/${DOCKER_IMAGE}:production</code></li>
                                    <li><code>${env.DOCKERHUB_CREDENTIALS_USR ?: 'username'}/${DOCKER_IMAGE}:stable</code></li>
                                    <li><code>${env.DOCKERHUB_CREDENTIALS_USR ?: 'username'}/${DOCKER_IMAGE}:latest</code></li>
                                </ul>
                            </div>
                            
                            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>🚀 Next Steps</h3>
                                <p>The containerized application has been successfully built, tested, and pushed to Docker Hub.</p>
                                <p>You can now deploy the application using:</p>
                                <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 3px;">docker run -p 5000:5000 ${env.DOCKERHUB_CREDENTIALS_USR ?: 'username'}/${DOCKER_IMAGE}:production</pre>
                            </div>
                            
                            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                                <p style="color: #6c757d; font-size: 12px;">
                                    This is an automated message from Jenkins CI/CD Pipeline.<br>
                                    Jenkins URL: <a href="${env.JENKINS_URL}">${env.JENKINS_URL}</a>
                                </p>
                            </div>
                        </body>
                        </html>
                        """,
                        to: emailList,
                        mimeType: 'text/html'
                    )
                } catch (Exception e) {
                    echo "⚠️ Failed to send email notification: ${e.getMessage()}"
                    echo "✅ Deployment completed successfully but email notification failed"
                }
            }
        }
        
        failure {
            script {
                echo "❌ Jenkins pipeline failed!"
                
                // Check if email credentials exist before sending
                try {
                    def emailList = env.NOTIFICATION_EMAIL ?: 'abdullahiqbal1133@gmail.com'
                    
                    // Send failure email notification
                    emailext (
                        subject: "❌ Deployment Failed - Student Performance ML [Build #${env.BUILD_NUMBER}]",
                        body: """
                        <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2 style="color: #dc3545;">❌ Deployment Failed!</h2>
                            
                            <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>🚨 Build Information</h3>
                                <ul>
                                    <li><strong>Project:</strong> Student Performance ML</li>
                                    <li><strong>Jenkins Build:</strong> #${env.BUILD_NUMBER}</li>
                                    <li><strong>GitHub Build:</strong> #${params.BUILD_NUMBER}</li>
                                    <li><strong>Git Commit:</strong> <code>${params.GIT_COMMIT}</code></li>
                                    <li><strong>Branch:</strong> ${params.GIT_BRANCH}</li>
                                    <li><strong>Repository:</strong> <a href="${params.REPOSITORY_URL}">${params.REPOSITORY_URL}</a></li>
                                    <li><strong>Failure Time:</strong> ${new Date()}</li>
                                </ul>
                            </div>
                            
                            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>🔍 Investigation Steps</h3>
                                <ol>
                                    <li>Check the Jenkins console output for detailed error messages</li>
                                    <li>Verify Docker Hub credentials and permissions</li>
                                    <li>Ensure the Docker image was built correctly by GitHub Actions</li>
                                    <li>Review application logs and container health</li>
                                </ol>
                            </div>
                            
                            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                                <p style="color: #6c757d; font-size: 12px;">
                                    This is an automated message from Jenkins CI/CD Pipeline.<br>
                                    Jenkins URL: <a href="${env.JENKINS_URL}">${env.JENKINS_URL}</a><br>
                                    Console Output: <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a>
                                </p>
                            </div>
                        </body>
                        </html>
                        """,
                        to: emailList,
                        mimeType: 'text/html'
                    )
                } catch (Exception e) {
                    echo "⚠️ Failed to send email notification: ${e.getMessage()}"
                    echo "❌ Pipeline failed and email notification also failed"
                }
            }
        }
        
        unstable {
            script {
                echo "⚠️ Jenkins pipeline completed with warnings!"
                
                // Check if email credentials exist before sending
                try {
                    def emailList = env.NOTIFICATION_EMAIL ?: 'abdullahiqbal1133@gmail.com'
                    
                    // Send warning email notification
                    emailext (
                        subject: "⚠️ Deployment Completed with Warnings - Student Performance ML [Build #${env.BUILD_NUMBER}]",
                        body: """
                        <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2 style="color: #ffc107;">⚠️ Deployment Completed with Warnings!</h2>
                            
                            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>📋 Build Information</h3>
                                <ul>
                                    <li><strong>Project:</strong> Student Performance ML</li>
                                    <li><strong>Jenkins Build:</strong> #${env.BUILD_NUMBER}</li>
                                    <li><strong>GitHub Build:</strong> #${params.BUILD_NUMBER}</li>
                                    <li><strong>Git Commit:</strong> <code>${params.GIT_COMMIT}</code></li>
                                    <li><strong>Branch:</strong> ${params.GIT_BRANCH}</li>
                                    <li><strong>Repository:</strong> <a href="${params.REPOSITORY_URL}">${params.REPOSITORY_URL}</a></li>
                                    <li><strong>Completion Time:</strong> ${new Date()}</li>
                                </ul>
                            </div>
                            
                            <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                <h3>⚠️ Warning Notice</h3>
                                <p>The deployment completed but with warnings. Please review the console output to understand what issues occurred.</p>
                                <p>The application may still be functional, but some components might not be working as expected.</p>
                            </div>
                            
                            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                                <p style="color: #6c757d; font-size: 12px;">
                                    This is an automated message from Jenkins CI/CD Pipeline.<br>
                                    Jenkins URL: <a href="${env.JENKINS_URL}">${env.JENKINS_URL}</a><br>
                                    Console Output: <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a>
                                </p>
                            </div>
                        </body>
                        </html>
                        """,
                        to: emailList,
                        mimeType: 'text/html'
                    )
                } catch (Exception e) {
                    echo "⚠️ Failed to send email notification: ${e.getMessage()}"
                    echo "⚠️ Pipeline completed with warnings and email notification failed"
                }
            }
        }
    }
}