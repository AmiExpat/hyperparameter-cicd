
# Hyperparameter Tuning and Deployment with Kubernetes

## Overview

This project aims to train a regression model to predict house prices using the California Housing dataset. We perform hyperparameter tuning to optimize the model's performance and run the tuning process in parallel using Kubernetes Jobs. The best model is then deployed for inference.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Build the Docker Image](#2-build-the-docker-image)
  - [3. Push or Load the Docker Image](#3-push-or-load-the-docker-image)
- [Hyperparameter Tuning with Kubernetes](#hyperparameter-tuning-with-kubernetes)
  - [1. Define Hyperparameter Grid](#1-define-hyperparameter-grid)
  - [2. Generate Kubernetes Job Files](#2-generate-kubernetes-job-files)
  - [3. Deploy Kubernetes Jobs](#3-deploy-kubernetes-jobs)
  - [4. Monitor Jobs and Collect Artifacts](#4-monitor-jobs-and-collect-artifacts)
- [Deploying the Best Model](#deploying-the-best-model)
  - [1. Build the Inference Docker Image](#1-build-the-inference-docker-image)
  - [2. Deploy the Inference Service](#2-deploy-the-inference-service)
  - [3. Test the Inference Service](#3-test-the-inference-service)
- [Reproducing the Pipelines](#reproducing-the-pipelines)
- [Artifact Storage](#artifact-storage)
- [Appendix](#appendix)
  - [Project Files](#project-files)
  - [Screenshots](#screenshots)

---

## Project Structure

```plaintext
hyperparameter/
├── Dockerfile
├── Dockerfile.inference
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── train.py
│   ├── hyperparameter_tuning.py
│   ├── inference.py
│   └── model_utils.py
├── kubernetes/
│   ├── job-template.yaml
│   ├── generate_jobs.py
│   ├── job_0.yaml
│   ├── job_1.yaml
│   ├── ...
│   └── inference-service.yaml
├── models/
├── artifacts/
```

---

## Prerequisites

- **Docker** installed and configured.
- **Kubernetes** cluster running (e.g., Minikube or a cloud-based Kubernetes service).
- **kubectl** command-line tool configured to interact with your cluster.
- **Python 3.13** (if you plan to run scripts locally).

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hyperparameter.git
cd hyperparameter
```

### 2. Build the Docker Image

```bash
docker build -t amibangladesh/hyperparameter:latest .
```

### 3. Push or Load the Docker Image

#### If Using Minikube:

```bash
minikube image load amibangladesh/hyperparameter:latest
```

#### If Using a Docker Registry:

- Tag the image if necessary:

  ```bash
  docker tag amibangladesh/hyperparameter:latest your_docker_registry/hyperparameter:latest
  ```

- Push the image to your registry:

  ```bash
  docker push your_docker_registry/hyperparameter:latest
  ```

---

## Hyperparameter Tuning with Kubernetes

### 1. Define Hyperparameter Grid

The hyperparameters we are tuning for XGBoost are:

- `n_estimators`: Number of trees in the ensemble.
- `max_depth`: Maximum depth of each tree.
- `learning_rate`: Step size shrinkage used in update to prevent overfitting.
- `subsample`: Subsample ratio of the training instances.

We define a small range for each hyperparameter to keep the computation manageable.

### 2. Generate Kubernetes Job Files

Run the script to generate Kubernetes job YAML files for each combination of hyperparameters.

```bash
python kubernetes/generate_jobs.py
```

This script will create `job_0.yaml`, `job_1.yaml`, ..., in the `kubernetes/` directory.

### 3. Deploy Kubernetes Jobs

Apply all the generated job configurations:

```bash
kubectl apply -f kubernetes/
```

**Note:** Ensure that only the job YAML files and necessary configurations are in the `kubernetes/` directory when running this command.

### 4. Monitor Jobs and Collect Artifacts

#### Monitor the Jobs

Check the status of the jobs:

```bash
kubectl get jobs
```

Check the pods:

```bash
kubectl get pods
```

#### View Logs

For each pod, you can view the logs to see the output:

```bash
kubectl logs <pod-name>
```

---

## Deploying the Best Model

### 1. Build the Inference Docker Image

After identifying the best model (e.g., by checking the MSE values in the metrics files), copy the corresponding model file to `models/best_model.joblib`.

Build the inference image:

```bash
docker build -f Dockerfile.inference -t amibangladesh/housing-inference:latest .
```

Push or load the image:

```bash
docker push amibangladesh/housing-inference:latest
```

### 2. Deploy the Inference Service

Apply the Kubernetes configuration:

```bash
kubectl apply -f kubernetes/inference-service.yaml
```

### 3. Test the Inference Service

Get the external IP of the service:

```bash
kubectl get services
```

Send a test request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"features": [-122.23, 37.88, 41, 880, 129, 322, 126, 8.3252]}' http://<external-ip>/predict
```

Expected response:

```json
{
  "prediction": [4.526]
}
```

---

## Reproducing the Pipelines

To reproduce the pipelines:

1. **Set Up the Environment:**

   - Ensure Docker and Kubernetes are installed.
   - Configure `kubectl` to interact with your cluster.

2. **Build and Push Docker Images:**

   - Build the training image: `docker build -t your_registry/hyperparameter:latest .`
   - Push the image to a registry accessible by your cluster.

3. **Generate Kubernetes Jobs:**

   - Run `python kubernetes/generate_jobs.py` to create job files.

4. **Deploy Jobs:**

   - Apply the job configurations: `kubectl apply -f kubernetes/`

5. **Monitor and Collect Artifacts:**

   - Use `kubectl get jobs` and `kubectl logs` to monitor.
   - Ensure artifacts are stored persistently.

6. **Deploy the Best Model:**

   - Build and push the inference image.
   - Deploy the inference service using Kubernetes.

---

## Artifact Storage

To store artifacts (models and metrics) persistently:

1. **Use Persistent Volumes:**

   - Define PersistentVolumes and PersistentVolumeClaims in Kubernetes.
   - Update `job-template.yaml` to use these volumes.

2. **Upload to Cloud Storage:**

   - Modify `hyperparameter_tuning.py` to upload files to a cloud storage bucket after training.

3. **Use a Shared File System:**

   - Configure a shared file system accessible by all pods.

---

## Appendix

### Project Files

- **Dockerfile**: Builds the image for training and hyperparameter tuning.
- **Dockerfile.inference**: Builds the image for serving the best model.
- **requirements.txt**: Lists Python dependencies.
- **src/**: Contains all source code.
  - **data_loader.py**: Loads the California Housing dataset.
  - **train.py**: Defines the training function.
  - **hyperparameter_tuning.py**: Orchestrates the tuning process.
  - **inference.py**: Provides an API endpoint for model inference.
  - **model_utils.py**: (Optional) Utility functions for model handling.
- **kubernetes/**: Kubernetes configurations.
  - **job-template.yaml**: Template for Kubernetes Jobs.
  - **generate_jobs.py**: Generates job YAML files from the template.
  - **job_*.yaml**: Generated job files for each hyperparameter combination.
  - **inference-service.yaml**: Deployment and Service configuration for inference.

---
