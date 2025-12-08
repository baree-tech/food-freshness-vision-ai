

---

```markdown
# Food Freshness Vision AI 🍎🥦

**Food Freshness Vision AI** is an end-to-end AI/ML project that automatically detects the freshness of food items using computer vision and deploys the solution on **Google Cloud Platform (GCP)** via **Cloud Run**. The project includes Dockerized deployment, CI/CD using **GitHub Actions**, and integration with **Artifact Registry**.

---

## **Project Features**
- **Food freshness classification** using deep learning models.
- **End-to-end pipeline**:
  - Data preprocessing
  - Model training and evaluation
  - Docker containerization
  - Deployment to Cloud Run
- **CI/CD with GitHub Actions** for automated builds and deployments.
- **Artifact Registry integration** for storing Docker images securely.
- **Cloud Run deployment** enabling scalable, serverless hosting.
- **Environment variables and service account authentication** for secure GCP access.

---

## **Technologies Used**
- **Python**: Main programming language
- **OpenCV, NumPy, Pandas**: Data processing and image handling
- **TensorFlow/Keras**: Deep learning model implementation
- **Docker**: Containerization
- **GitHub Actions**: CI/CD workflows
- **GCP**:
  - Cloud Run (Serverless deployment)
  - Artifact Registry (Docker image repository)
  - IAM & Service Accounts (Security and permissions management)
  - Cloud Storage (Optional: for model storage)

---

## **Repository Structure**
```

.
├── .github/workflows/deploy.yaml   # CI/CD workflow for build & deploy
├── Dockerfile                      # Docker container configuration
├── app.py                           # Flask app for inference
├── food_freshness.ipynb            # Notebook for model training/testing
├── requirements.txt                # Python dependencies
└── README.md                        # Project documentation

````

---

## **Setup & Deployment**
1. Clone the repository:
```bash
git clone https://github.com/baree-tech/food-freshness-vision-ai.git
cd food-freshness-vision-ai
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. **Docker Build & Push** (via GitHub Actions):

   * GitHub Actions workflow `.github/workflows/deploy.yaml` automatically builds and pushes the Docker image to Artifact Registry.
   * Deploys to **Cloud Run** for serverless hosting.

4. Access the deployed application via the Cloud Run URL (publicly accessible).

---

## **CI/CD Workflow Highlights**

* Authenticates to GCP using **service account key** stored in GitHub Secrets.
* Configures Docker for Artifact Registry authentication.
* Builds Docker image tagged with **Git commit SHA**.
* Pushes image to **Artifact Registry**.
* Deploys automatically to **Cloud Run** with 1Gi memory and **allow-unauthenticated** access.
* Triggered automatically on push to the `main` branch.

---

## **Service Account Roles**

The GitHub Actions deploy service account includes:

* `roles/run.admin`
* `roles/artifactregistry.writer`
* `roles/storage.objectViewer`
* `roles/iam.serviceAccountUser`

---

## **Learning & Achievements**

* Hands-on experience with **end-to-end AI/ML deployment**.
* Learned **GCP IAM, Artifact Registry, Cloud Run** in a production-ready setup.
* Implemented **CI/CD pipeline using GitHub Actions** for Docker-based deployments.
* Solid understanding of **service accounts, permissions, and security best practices**.
* Experience in **version-controlled deployment**, linking GitHub commits to production builds.

---

## **Future Work**

* Extend model to detect **more food categories and freshness levels**.
* Integrate with a **mobile/web app** for real-time scanning.
* Add **notifications or analytics dashboard** for inventory monitoring.

---

## **Author**

Bareera Mushthak

* AI/ML Engineer | Computer Vision | Cloud Deployment | CI/CD | Python | GCP

```

---


```
