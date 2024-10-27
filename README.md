# CI/CD Pipeline for Model Deployment

## Overview

This repository demonstrates a CI/CD pipeline for deploying a regression model trained to predict house prices.

### Tools and Technologies

- **GitHub Actions** for CI/CD
- **Docker** for containerization
- **Kubernetes** for deployment
- **pytest** for testing

## Architecture

1. **Continuous Integration:** 
   - Runs tests on new code.
   - Compares accuracy of the new model with the previous model.

2. **Continuous Deployment:**
   - Deploys the new model if it outperforms the previous one.
   - Uses Kubernetes for deployment.

## Challenges

- Handling persistent model artifacts in CI/CD.
- Ensuring compatibility with Python 3.13.

## Reproducing the Pipeline

1. Clone the repository and navigate to the project directory.
2. Set up a Kubernetes cluster (e.g., Minikube).
3. Push code changes to the repository to trigger the CI/CD workflow.
