# GitHub Secrets Configuration

This document explains how to set up the required secrets for the CI/CD pipeline to work properly.

## Required Secrets

### Docker Hub Secrets (Required for Docker builds)
- **DOCKERHUB_USERNAME**: Your Docker Hub username
- **DOCKERHUB_TOKEN**: Your Docker Hub access token (not password)

### Jenkins Secrets (Optional - for Jenkins integration)
- **JENKINS_URL**: Your Jenkins server URL (e.g., `https://jenkins.example.com`)
- **JENKINS_USER**: Jenkins username with API access
- **JENKINS_TOKEN**: Jenkins API token
- **JENKINS_JOB_NAME**: Name of the Jenkins job to trigger

## How to Configure Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** > **Actions**
4. Click **New repository secret**
5. Add each secret with the name and value

## Docker Hub Setup

### Step 1: Create Docker Hub Access Token
1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** > **Security**
3. Click **New Access Token**
4. Give it a name (e.g., "GitHub Actions")
5. Select **Read, Write, Delete** permissions
6. Copy the generated token

### Step 2: Add Secrets to GitHub
- **DOCKERHUB_USERNAME**: Your Docker Hub username
- **DOCKERHUB_TOKEN**: The access token you just created

## Jenkins Setup (Optional)

### Step 1: Get Jenkins API Token
1. Log in to your Jenkins instance
2. Click on your username in the top right
3. Click **Configure**
4. Under **API Token**, click **Add new Token**
5. Give it a name and click **Generate**
6. Copy the generated token

### Step 2: Add Secrets to GitHub
- **JENKINS_URL**: Your Jenkins server URL (include https://)
- **JENKINS_USER**: Your Jenkins username
- **JENKINS_TOKEN**: The API token you just created
- **JENKINS_JOB_NAME**: The name of your Jenkins job

## Pipeline Behavior

### With Docker Hub Secrets Configured
✅ The build job will:
- Build and push Docker images to Docker Hub
- Tag images with build number and commit SHA

### Without Docker Hub Secrets
❌ The build job will:
- Fail with clear error message about missing credentials
- Stop the pipeline execution

### With Jenkins Secrets Configured
✅ The trigger-jenkins job will:
- Send build parameters to Jenkins
- Trigger the specified Jenkins job
- Provide success/failure feedback

### Without Jenkins Secrets
⚠️ The trigger-jenkins job will:
- Skip the Jenkins trigger step
- Display a helpful message about configuring Jenkins
- Continue without errors

## Troubleshooting

### "Username and password required" Error
This means Docker Hub secrets are missing or incorrect:
1. Verify DOCKERHUB_USERNAME is set correctly
2. Verify DOCKERHUB_TOKEN is a valid access token (not password)
3. Make sure the token has the correct permissions

### "No host part in the URL" Error
This means Jenkins URL is missing or malformed:
1. Verify JENKINS_URL includes the protocol (https://)
2. Verify JENKINS_URL doesn't have trailing slashes
3. Test the URL in your browser

### Jenkins Trigger Fails
1. Verify Jenkins credentials are correct
2. Verify the Jenkins job name exists
3. Check Jenkins logs for authentication issues
4. Ensure the Jenkins user has permission to trigger builds

## Security Notes

- Never commit secrets to your repository
- Use access tokens instead of passwords
- Regularly rotate your tokens
- Use minimal required permissions for tokens
- Monitor secret usage in repository settings