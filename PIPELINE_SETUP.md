# CI/CD Pipeline Configuration Guide

This guide walks you through setting up the complete CI/CD pipeline for the Student Performance ML project, including GitHub Actions and Jenkins integration.

## 🔄 Pipeline Overview

The CI/CD pipeline follows this flow:

```
1. Pull Request → GitHub Actions (Automated Testing)
2. Merge to Master → GitHub Actions (Build & Push Docker Image)
3. GitHub Actions → Trigger Jenkins Job
4. Jenkins → Containerize, Test, Deploy & Email Notification
```

## 📋 Prerequisites

### Required Tools
- GitHub repository with admin access
- Jenkins server with Docker support
- Docker Hub account
- Email server (SMTP) access for notifications

### Required Permissions
- GitHub: Repository admin access to configure secrets and workflows
- Jenkins: Admin access to create jobs and configure credentials
- Docker Hub: Push/pull permissions for your repositories

## 🚀 Step 1: GitHub Repository Setup

### 1.1 Configure Branch Protection Rules

1. Go to your GitHub repository
2. Navigate to **Settings** → **Branches**
3. Click **Add rule** for `master` branch
4. Enable the following:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

### 1.2 Configure Repository Secrets

Navigate to **Settings** → **Secrets and variables** → **Actions** and add:

#### Required Secrets (Docker Hub)
```
DOCKERHUB_USERNAME = your-dockerhub-username
DOCKERHUB_TOKEN = your-dockerhub-access-token
```

#### Optional Secrets (Jenkins Integration)
```
JENKINS_URL = https://your-jenkins-server.com
JENKINS_USER = jenkins-username
JENKINS_TOKEN = jenkins-api-token
JENKINS_JOB_NAME = student-performance-ml-deploy
```

### 1.3 Docker Hub Setup

1. **Create Access Token:**
   - Login to [Docker Hub](https://hub.docker.com/)
   - Go to **Account Settings** → **Security**
   - Click **New Access Token**
   - Name: `GitHub Actions CI/CD`
   - Permissions: **Read, Write, Delete**
   - Copy the generated token

2. **Create Repository:**
   - Go to **Repositories** → **Create Repository**
   - Name: `student-performance-ml`
   - Visibility: Public or Private (as needed)

## 🔧 Step 2: Jenkins Configuration

### 2.1 Install Required Plugins

In Jenkins, go to **Manage Jenkins** → **Manage Plugins** and install:

- ✅ Docker Pipeline Plugin
- ✅ Email Extension Plugin  
- ✅ Pipeline Plugin
- ✅ Git Plugin
- ✅ Credentials Binding Plugin

### 2.2 Configure Jenkins Credentials

Navigate to **Manage Jenkins** → **Manage Credentials** → **Global** and add:

#### 2.2.1 Docker Hub Credentials
- **Type:** Username with password
- **ID:** `dockerhub-credentials`
- **Username:** Your Docker Hub username
- **Password:** Your Docker Hub access token

#### 2.2.2 Admin Email List
- **Type:** Secret text
- **ID:** `admin-email-list`
- **Secret:** Comma-separated emails (e.g., `admin@company.com,devops@company.com`)

### 2.3 Configure Email Settings

1. **System Configuration:**
   - Go to **Manage Jenkins** → **Configure System**
   - Find **Extended E-mail Notification** section
   - Configure SMTP server settings:
     ```
     SMTP server: your-smtp-server.com
     SMTP port: 587 (or 465 for SSL)
     Username: your-email@company.com
     Password: your-email-password
     ```

2. **Test Email Configuration:**
   - Check **Use SSL** if required
   - Click **Test configuration by sending test e-mail**
   - Verify email delivery

### 2.4 Create Jenkins Job

1. **Create New Job:**
   - Go to Jenkins dashboard
   - Click **New Item**
   - Name: `student-performance-ml-deploy`
   - Type: **Pipeline**
   - Click **OK**

2. **Configure Pipeline:**
   - **Pipeline Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** Your GitHub repository URL
   - **Branch:** `*/master`
   - **Script Path:** `Jenkinsfile`

3. **Enable Parameters:**
   - Check **This project is parameterized**
   - The Jenkinsfile will automatically handle the parameters

4. **Build Triggers:**
   - Check **Trigger builds remotely (e.g., from scripts)**
   - Set **Authentication Token** (optional but recommended)

## 🔍 Step 3: Testing the Pipeline

### 3.1 Test Pull Request Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/test-pipeline
   ```

2. Make a small change (e.g., update README.md)

3. Push and create a pull request:
   ```bash
   git add .
   git commit -m "Test: CI/CD pipeline"
   git push origin feature/test-pipeline
   ```

4. Create a pull request in GitHub

5. **Expected Result:** GitHub Actions should run automated tests

### 3.2 Test Master Merge Workflow

1. Merge the pull request to master

2. **Expected Results:**
   - ✅ GitHub Actions builds and pushes Docker image
   - ✅ GitHub Actions triggers Jenkins job
   - ✅ Jenkins pulls image, tests it, and pushes production tags
   - ✅ Email notification sent to administrators

## 📧 Email Notification Examples

### Success Email
```
Subject: ✅ Deployment Successful - Student Performance ML [Build #123]

Content includes:
- Build information (commit, branch, build numbers)
- Docker image tags available
- Next deployment steps
- Links to Jenkins and repository
```

### Failure Email
```
Subject: ❌ Deployment Failed - Student Performance ML [Build #123]

Content includes:
- Error details and investigation steps
- Links to console output and logs
- Troubleshooting guidance
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Username and password required" Error
- **Cause:** Missing or incorrect Docker Hub credentials
- **Solution:** Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets

#### 2. Jenkins Job Not Triggered
- **Cause:** Missing Jenkins secrets or incorrect configuration
- **Solution:** Verify all Jenkins secrets are set correctly

#### 3. Email Notifications Not Sent
- **Cause:** SMTP configuration issues or missing email credentials
- **Solution:** Test email configuration in Jenkins system settings

#### 4. Docker Image Pull Fails in Jenkins
- **Cause:** Image not found or Docker Hub access issues
- **Solution:** Verify image was built successfully by GitHub Actions

### Debug Commands

#### Check Docker Images
```bash
# List images on Docker Hub
curl -s "https://registry-1.docker.io/v2/your-username/student-performance-ml/tags/list" | jq '.'

# Pull and inspect locally
docker pull your-username/student-performance-ml:latest
docker inspect your-username/student-performance-ml:latest
```

#### Test Jenkins API
```bash
# Test Jenkins connectivity
curl -u username:token https://your-jenkins-server.com/api/json

# Trigger job manually
curl -X POST -u username:token \
  "https://your-jenkins-server.com/job/student-performance-ml-deploy/buildWithParameters" \
  -d "DOCKER_IMAGE_TAG=latest"
```

## 🔐 Security Best Practices

1. **Use Access Tokens:** Never use passwords in CI/CD secrets
2. **Minimal Permissions:** Grant only necessary permissions to tokens
3. **Regular Rotation:** Rotate tokens and credentials regularly
4. **Secret Management:** Use proper secret management for production
5. **Network Security:** Ensure Jenkins is properly secured and accessible

## 📈 Monitoring and Maintenance

### Pipeline Metrics to Monitor
- ✅ Test success rate
- ✅ Build time duration
- ✅ Deployment frequency
- ✅ Mean time to recovery (MTTR)

### Regular Maintenance Tasks
- Update dependencies in `requirements.txt`
- Rotate credentials and tokens
- Review and update pipeline configurations
- Monitor resource usage and costs

## 🎯 Next Steps

After successful setup:

1. **Set up monitoring** for your deployed applications
2. **Configure staging environment** for additional testing
3. **Implement blue-green deployment** for zero-downtime updates
4. **Add performance testing** to the pipeline
5. **Set up log aggregation** for better debugging

---

For additional help, refer to:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jenkins Pipeline Documentation](https://jenkins.io/doc/book/pipeline/)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)