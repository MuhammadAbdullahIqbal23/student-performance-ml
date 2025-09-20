# CI/CD Pipeline Setup Guide

This document provides comprehensive instructions for setting up and configuring the CI/CD pipeline for the Student Performance ML project.

## Overview

The CI/CD pipeline consists of two main components:

1. **GitHub Actions**: Handles automated testing on pull requests and triggers Jenkins on master branch merges
2. **Jenkins**: Manages Docker containerization, deployment to Docker Hub, and email notifications

## Pipeline Flow

```
Pull Request → GitHub Actions (Tests) → Merge to Master → GitHub Actions (Trigger Jenkins) → Jenkins (Build & Deploy) → Email Notification
```

## GitHub Actions Configuration

### Required Secrets

Configure the following secrets in your GitHub repository settings:

#### Docker Hub Secrets
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token (not password)

#### Jenkins Integration Secrets
- `JENKINS_URL`: Full URL to your Jenkins instance (e.g., `https://jenkins.example.com`)
- `JENKINS_USER`: Jenkins username with build permissions
- `JENKINS_TOKEN`: Jenkins API token for the user
- `JENKINS_JOB_NAME`: Name of the Jenkins job (e.g., `student-performance-ml-deploy`)

### Setting up GitHub Secrets

1. Navigate to your repository on GitHub
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with the corresponding name and value

## Jenkins Configuration

### Required Plugins

Ensure the following Jenkins plugins are installed:

- **Docker Pipeline Plugin**: For Docker operations
- **Email Extension Plugin**: For email notifications
- **Pipeline Plugin**: For pipeline support
- **Git Plugin**: For Git integration
- **Credentials Plugin**: For managing secrets

### Required Credentials

Configure the following credentials in Jenkins:

#### 1. Docker Hub Credentials (`dockerhub-credentials`)
- Type: Username with password
- Username: Your Docker Hub username
- Password: Your Docker Hub access token

#### 2. Administrator Email List (`admin-email-list`)
- Type: Secret text
- Secret: Comma-separated list of admin emails (e.g., `admin@company.com,devops@company.com`)

### Creating Jenkins Job

1. **Create New Job**
   - Go to Jenkins dashboard
   - Click "New Item"
   - Enter job name (e.g., `student-performance-ml-deploy`)
   - Select "Pipeline"
   - Click "OK"

2. **Configure Pipeline**
   - In the job configuration, scroll to "Pipeline" section
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: Your GitHub repository URL
   - Credentials: Add GitHub credentials if repository is private
   - Branch: `*/master` (or `*/main`)
   - Script Path: `Jenkinsfile`

3. **Enable Build Parameters**
   - Check "This project is parameterized"
   - Add String parameters:
     - `BRANCH_NAME` (default: master)
     - `COMMIT_SHA` (default: empty)
     - `COMMIT_MESSAGE` (default: empty)

4. **Configure Build Triggers**
   - Check "Trigger builds remotely"
   - Set authentication token (optional but recommended)

## Email Configuration

### Jenkins Email Setup

1. **Configure System Email**
   - Go to Manage Jenkins → Configure System
   - Find "Extended E-mail Notification" section
   - Configure SMTP server settings:
     - SMTP server: Your SMTP server (e.g., `smtp.gmail.com`)
     - Default user e-mail suffix: Your domain (e.g., `@company.com`)
     - SMTP port: Usually 587 for TLS or 465 for SSL
     - Username/Password: SMTP credentials

2. **Test Email Configuration**
   - Use "Test configuration by sending test e-mail"
   - Verify emails are received correctly

### Email Templates

The pipeline includes custom email templates for:
- **Success notifications**: Sent when build and deployment complete successfully
- **Failure notifications**: Sent when any stage fails
- **Unstable notifications**: Sent when build completes with warnings

## Docker Hub Setup

### Create Repository

1. Log in to Docker Hub
2. Create a new repository named `student-performance-ml`
3. Set visibility (public or private as needed)
4. Note the repository URL for reference

### Generate Access Token

1. Go to Account Settings → Security
2. Click "New Access Token"
3. Enter description (e.g., "Jenkins CI/CD")
4. Select appropriate permissions
5. Copy the generated token (use this as `DOCKERHUB_TOKEN`)

## Workflow Triggers

### Automated Testing (Pull Requests)

- **Trigger**: Any pull request to `master`, `main`, or `dev` branches
- **Actions**:
  - Run tests on Python 3.8, 3.9, and 3.10
  - Execute flake8 linting
  - Run pylint code analysis
  - Block merge if tests fail

### Jenkins Deployment (Master Merge)

- **Trigger**: Push to `master` or `main` branch
- **Actions**:
  - Trigger Jenkins job via API call
  - Pass branch name, commit SHA, and commit message
  - Jenkins builds and deploys Docker image

## Monitoring and Troubleshooting

### GitHub Actions

- **View workflow runs**: Repository → Actions tab
- **Check logs**: Click on specific workflow run
- **Debug failures**: Check individual step logs

### Jenkins

- **View build history**: Jenkins job → Build History
- **Check console output**: Click on specific build number → Console Output
- **Monitor email delivery**: Check email logs in Jenkins system log

### Common Issues

1. **GitHub Actions fails to trigger Jenkins**
   - Verify Jenkins URL and credentials
   - Check Jenkins job exists and is configured correctly
   - Ensure Jenkins is accessible from GitHub (public URL)

2. **Docker push fails**
   - Verify Docker Hub credentials
   - Check repository name and permissions
   - Ensure Docker Hub token has push permissions

3. **Email notifications not sent**
   - Verify SMTP configuration
   - Check email credentials
   - Test email configuration in Jenkins

## Security Considerations

### Secrets Management

- Never commit secrets to repository
- Use GitHub Secrets for sensitive information
- Rotate tokens and passwords regularly
- Limit permissions to minimum required

### Network Security

- Use HTTPS for all communications
- Restrict Jenkins access to authorized users
- Use VPN or firewall rules for additional security

### Container Security

- Regularly update base images
- Scan containers for vulnerabilities
- Use non-root user in containers
- Implement proper secret management in containers

## Maintenance

### Regular Tasks

1. **Update Dependencies**
   - Review and update Python packages
   - Update base Docker images
   - Update GitHub Actions versions

2. **Monitor Pipeline Performance**
   - Check build times and optimize if needed
   - Review test coverage and add tests as needed
   - Monitor resource usage

3. **Security Updates**
   - Rotate access tokens quarterly
   - Review and update permissions
   - Scan for security vulnerabilities

### Backup and Recovery

- **Jenkins Configuration**: Export job configurations regularly
- **Secrets**: Maintain secure backup of all credentials
- **Docker Images**: Keep tagged releases for rollback capability

## Support and Contact

For issues with the CI/CD pipeline:

1. Check the troubleshooting section above
2. Review GitHub Actions and Jenkins logs
3. Contact the DevOps team with specific error messages
4. Create an issue in the repository for pipeline improvements

---

## Quick Reference

### GitHub Actions Workflow File
- Location: `.github/workflows/ci-cd.yml`
- Triggers: Pull requests and pushes to master/main

### Jenkins Pipeline File
- Location: `Jenkinsfile` (repository root)
- Stages: Checkout → Build → Test → Push → Cleanup

### Required Secrets
- GitHub: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `JENKINS_URL`, `JENKINS_USER`, `JENKINS_TOKEN`, `JENKINS_JOB_NAME`
- Jenkins: `dockerhub-credentials`, `admin-email-list`

### Key Features
- ✅ Automated testing on pull requests
- ✅ Docker containerization and deployment
- ✅ Multi-tag Docker image publishing
- ✅ Email notifications for build status
- ✅ Comprehensive error handling and cleanup