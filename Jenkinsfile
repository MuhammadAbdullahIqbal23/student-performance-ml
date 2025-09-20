pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'student-performance-ml'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_LATEST = 'latest'
        DOCKERHUB_CREDENTIALS = credentials('muhammadabdullahiqbal-dockerhub')
        ADMIN_EMAIL_LIST = credentials('admin-email-list')
    }
    
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'master', description: 'Git branch name')
        string(name: 'COMMIT_SHA', defaultValue: '', description: 'Git commit SHA')
        string(name: 'COMMIT_MESSAGE', defaultValue: '', description: 'Git commit message')
        string(name: 'GITHUB_RUN_ID', defaultValue: '', description: 'GitHub Actions run ID')
        string(name: 'GITHUB_RUN_NUMBER', defaultValue: '', description: 'GitHub Actions run number')
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('🔍 Checkout & Validation') {
            steps {
                script {
                    echo "🚀 Starting Jenkins Containerization Job"
                    echo "========================================="
                    echo "Triggered by: GitHub Actions"
                    echo "Branch: ${params.BRANCH_NAME}"
                    echo "Commit: ${params.COMMIT_SHA}"
                    echo "Message: ${params.COMMIT_MESSAGE}"
                    echo "GitHub Run: ${params.GITHUB_RUN_NUMBER}"
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
        
        stage('🐳 Docker Environment Setup') {
            steps {
                script {
                    env.IMAGE_NAME = "${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}"
                    env.IMAGE_TAG_BUILD = "${env.IMAGE_NAME}:build-${DOCKER_TAG}"
                    env.IMAGE_TAG_LATEST = "${env.IMAGE_NAME}:${DOCKER_LATEST}"
                    env.IMAGE_TAG_COMMIT = "${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                    env.IMAGE_TAG_GITHUB = "${env.IMAGE_NAME}:github-${params.GITHUB_RUN_NUMBER}"
                }
                
                echo "🏗️ Docker Build Configuration:"
                echo "Repository: ${env.IMAGE_NAME}"
                echo "Build Tag: ${env.IMAGE_TAG_BUILD}"
                echo "Latest Tag: ${env.IMAGE_TAG_LATEST}"
                echo "Commit Tag: ${env.IMAGE_TAG_COMMIT}"
                echo "GitHub Tag: ${env.IMAGE_TAG_GITHUB}"
            }
        }
        
        stage('🏗️ Build Docker Image') {
            steps {
                script {
                    echo "🔨 Building Docker image for production deployment..."
                    
                    // Build the Docker image
                    def image = docker.build("${env.IMAGE_TAG_BUILD}")
                    
                    // Tag the image with multiple tags for different purposes
                    sh """
                        docker tag ${env.IMAGE_TAG_BUILD} ${env.IMAGE_TAG_LATEST}
                        docker tag ${env.IMAGE_TAG_BUILD} ${env.IMAGE_TAG_COMMIT}
                        docker tag ${env.IMAGE_TAG_BUILD} ${env.IMAGE_TAG_GITHUB}
                    """
                    
                    echo "✅ Docker image built and tagged successfully"
                }
            }
        }
        
        stage('🧪 Container Testing') {
            steps {
                script {
                    echo "🔍 Testing containerized application..."
                    
                    // Run comprehensive tests on the container
                    sh """
                        # Start test container
                        docker run --rm -d --name test-container-${BUILD_NUMBER} -p 5002:5000 ${env.IMAGE_TAG_BUILD}
                        sleep 15
                        
                        echo "Testing application endpoints..."
                        
                        # Test health endpoint
                        curl -f http://localhost:5002/health || (echo "Health check failed" && docker logs test-container-${BUILD_NUMBER} && exit 1)
                        
                        # Test model info endpoint
                        curl -f http://localhost:5002/model/info || (echo "Model info failed" && docker logs test-container-${BUILD_NUMBER} && exit 1)
                        
                        # Test sample data generation
                        curl -f http://localhost:5002/generate/sample || (echo "Sample generation failed" && docker logs test-container-${BUILD_NUMBER} && exit 1)
                        
                        echo "✅ All container tests passed"
                        
                        # Stop test container
                        docker stop test-container-${BUILD_NUMBER}
                    """
                }
            }
            post {
                always {
                    sh "docker stop test-container-${BUILD_NUMBER} || true"
                    sh "docker rm test-container-${BUILD_NUMBER} || true"
                }
            }
        }
        
        stage('📤 Push to Docker Hub') {
            steps {
                script {
                    echo "🚀 Pushing Docker images to Docker Hub..."
                    
                    docker.withRegistry('https://index.docker.io/v1/', 'muhammadabdullahiqbal-dockerhub') {
                        // Push all tags
                        sh """
                            echo "Pushing build-specific tag..."
                            docker push ${env.IMAGE_TAG_BUILD}
                            
                            echo "Pushing latest tag..."
                            docker push ${env.IMAGE_TAG_LATEST}
                            
                            echo "Pushing commit-specific tag..."
                            docker push ${env.IMAGE_TAG_COMMIT}
                            
                            echo "Pushing GitHub-specific tag..."
                            docker push ${env.IMAGE_TAG_GITHUB}
                        """
                    }
                    
                    echo "✅ All Docker images pushed successfully to Docker Hub"
                }
            }
        }
        
        stage('🧹 Cleanup') {
            steps {
                script {
                    echo "🧽 Cleaning up local Docker images..."
                    
                    sh """
                        docker rmi ${env.IMAGE_TAG_BUILD} || true
                        docker rmi ${env.IMAGE_TAG_LATEST} || true
                        docker rmi ${env.IMAGE_TAG_COMMIT} || true
                        docker rmi ${env.IMAGE_TAG_GITHUB} || true
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
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 20px; margin: 20px 0;">
                        <h2 style="color: #155724; margin-top: 0;">🎉 Jenkins Deployment Successful</h2>
                    </div>
                    
                    <h3>📋 Build Information</h3>
                    <table style="border-collapse: collapse; width: 100%;">
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Project:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">Student Performance ML</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Jenkins Build:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">#${BUILD_NUMBER}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>GitHub Actions Run:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">#${params.GITHUB_RUN_NUMBER}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Branch:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${params.BRANCH_NAME}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Commit SHA:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${params.COMMIT_SHA}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Commit Message:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${params.COMMIT_MESSAGE}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Build Duration:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${buildDuration}</td></tr>
                    </table>
                    
                    <h3>🐳 Docker Images Published</h3>
                    <ul>
                        <li><code>${env.IMAGE_TAG_BUILD}</code> - Build-specific tag</li>
                        <li><code>${env.IMAGE_TAG_LATEST}</code> - Latest production tag</li>
                        <li><code>${env.IMAGE_TAG_COMMIT}</code> - Commit-specific tag</li>
                        <li><code>${env.IMAGE_TAG_GITHUB}</code> - GitHub Actions tag</li>
                    </ul>
                    
                    <h3>🔗 Quick Links</h3>
                    <ul>
                        <li><a href="${BUILD_URL}">📊 Jenkins Build Details</a></li>
                        <li><a href="https://hub.docker.com/r/${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}">🐳 Docker Hub Repository</a></li>
                        <li><a href="https://github.com/MuhammadAbdullahIqbal23/student-performance-ml/actions/runs/${params.GITHUB_RUN_ID}">🚀 GitHub Actions Run</a></li>
                    </ul>
                    
                    <h3>🚀 Deployment Status</h3>
                    <div style="background-color: #d1ecf1; border: 1px solid #bee5eb; border-radius: 5px; padding: 15px;">
                        <p style="margin: 0;"><strong>✅ Application Successfully Containerized and Deployed</strong></p>
                        <p style="margin: 5px 0 0 0;">The Student Performance ML application is now available on Docker Hub with multiple tags for different deployment scenarios.</p>
                    </div>
                    
                    <hr style="margin: 30px 0;">
                    <p style="color: #6c757d; font-size: 12px;"><em>This is an automated notification from Jenkins CI/CD Pipeline<br>
                    Triggered by successful merge to master branch</em></p>
                </body>
                </html>
                """
                
                emailext (
                    subject: "✅ Jenkins Build #${BUILD_NUMBER} - SUCCESS - Student Performance ML Deployed",
                    body: emailBody,
                    mimeType: 'text/html',
                    to: "${ADMIN_EMAIL_LIST}",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ]
                )
                
                echo "📧 Success notification email sent to administrators"
            }
        }
        
        failure {
            script {
                def buildDuration = currentBuild.durationString.replace(' and counting', '')
                def emailBody = """
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 20px; margin: 20px 0;">
                        <h2 style="color: #721c24; margin-top: 0;">❌ Jenkins Deployment Failed</h2>
                    </div>
                    
                    <h3>📋 Build Information</h3>
                    <table style="border-collapse: collapse; width: 100%;">
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Project:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">Student Performance ML</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Jenkins Build:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">#${BUILD_NUMBER}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>GitHub Actions Run:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">#${params.GITHUB_RUN_NUMBER}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Branch:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${params.BRANCH_NAME}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Failed Stage:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${env.STAGE_NAME ?: 'Unknown'}</td></tr>
                        <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Build Duration:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${buildDuration}</td></tr>
                    </table>
                    
                    <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0; color: #721c24;"><strong>🚨 Immediate Attention Required!</strong></p>
                        <p style="margin: 5px 0 0 0; color: #721c24;">The containerization and deployment process has failed. Please review the build logs and fix the issues.</p>
                    </div>
                    
                    <h3>🔗 Troubleshooting Links</h3>
                    <ul>
                        <li><a href="${BUILD_URL}console">🔍 Jenkins Console Output</a></li>
                        <li><a href="${BUILD_URL}">📊 Jenkins Build Details</a></li>
                        <li><a href="https://github.com/MuhammadAbdullahIqbal23/student-performance-ml/actions/runs/${params.GITHUB_RUN_ID}">🚀 GitHub Actions Run</a></li>
                    </ul>
                    
                    <hr style="margin: 30px 0;">
                    <p style="color: #6c757d; font-size: 12px;"><em>This is an automated notification from Jenkins CI/CD Pipeline</em></p>
                </body>
                </html>
                """
                
                emailext (
                    subject: "❌ Jenkins Build #${BUILD_NUMBER} - FAILED - Student Performance ML",
                    body: emailBody,
                    mimeType: 'text/html',
                    to: "${ADMIN_EMAIL_LIST}",
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ]
                )
                
                echo "📧 Failure notification email sent to administrators"
            }
        }
        
        always {
            // Archive build information
            script {
                writeFile file: 'build-info.txt', text: """
Build Information:
==================
Jenkins Build: ${BUILD_NUMBER}
GitHub Actions Run: ${params.GITHUB_RUN_NUMBER}
Branch: ${params.BRANCH_NAME}
Commit: ${params.COMMIT_SHA}
Commit Message: ${params.COMMIT_MESSAGE}
Build Status: ${currentBuild.currentResult}
Build Duration: ${currentBuild.durationString}
Docker Images:
- ${env.IMAGE_TAG_BUILD}
- ${env.IMAGE_TAG_LATEST}
- ${env.IMAGE_TAG_COMMIT}
- ${env.IMAGE_TAG_GITHUB}
"""
                archiveArtifacts artifacts: 'build-info.txt', fingerprint: true
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