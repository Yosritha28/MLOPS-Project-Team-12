# ResumeIQ – AI-Powered Resume Analysis and Job Matching Platform



<p align="center">

&#x20; <strong>AI-Powered Resume Screening | Explainable Matching | MLOps | Responsive Web \& Mobile PWA</strong>

</p>



\## 1. Project Overview



\*\*ResumeIQ\*\* is an AI-powered resume analysis and job-matching platform designed to simplify and improve the recruitment screening process.



Traditional resume screening requires recruiters to manually examine large numbers of resumes and compare candidate qualifications against job descriptions. This process can be time-consuming, inconsistent and heavily dependent on exact keyword matching.



ResumeIQ addresses these challenges using Natural Language Processing (NLP), Machine Learning and MLOps techniques to analyze resumes, extract relevant information, calculate candidate-job compatibility scores and generate ranked recommendations.



The platform combines \*\*TF-IDF, Sentence-BERT (SBERT) and skill-based matching\*\* to evaluate both lexical and semantic similarity between resumes and job descriptions.



It also provides explainable matching results, including matched skills, missing skills, component scores and supporting evidence.



ResumeIQ is designed as a responsive Progressive Web Application (PWA), allowing candidates and recruiters to access the platform through desktop, laptop and mobile browsers.



\## 2. Project Objectives



\- Automate resume parsing and information extraction.

\- Extract skills, education, experience and project information from resumes.

\- Analyze job descriptions and identify required qualifications and skills.

\- Implement lexical similarity using TF-IDF.

\- Implement semantic similarity using Sentence-BERT.

\- Develop a hybrid matching mechanism combining multiple similarity components.

\- Rank candidates according to their compatibility with job requirements.

\- Generate explainable results using matched and missing skills.

\- Support fairness evaluation and feedback-driven improvement.

\- Implement experiment tracking, data/model versioning and reproducible workflows.

\- Integrate automated testing, CI/CD and containerization.

\- Provide a responsive application for desktop and mobile browsers.



\## 3. Key Features



\### 3.1 Resume Analysis



\- Accepts candidate resume documents in PDF and DOCX formats.

\- Extracts relevant textual information.

\- Identifies skills, education, work experience and projects.

\- Preprocesses extracted text for NLP operations.



\### 3.2 Job Description Analysis



\- Processes recruiter-provided job descriptions.

\- Identifies required and preferred skills.

\- Extracts role-specific qualifications and experience requirements.

\- Converts job descriptions into structured information for matching.



\### 3.3 AI-Based Resume Matching



ResumeIQ uses three matching components:



\*\*TF-IDF Similarity\*\*



Measures lexical similarity between resume content and job descriptions using term-frequency and inverse-document-frequency representations.



\*\*Sentence-BERT (SBERT)\*\*



Uses semantic embeddings to identify similarities between sentences and phrases, even when different words are used to express related concepts.



\*\*Skill-Based Matching\*\*



Compares extracted candidate skills against the required and preferred skills in the job description.



\### 3.4 Hybrid Matching



The hybrid matching mechanism combines the three components using configurable weights.



Conceptually:



`Hybrid Score = (w\_tfidf × TF-IDF) + (w\_sbert × SBERT) + (w\_skills × Skill Match)`



The weights are validated and configured to sum to 1.0.



\### 3.5 Explainable Results



The matching output can include:



\- Overall compatibility score.

\- TF-IDF similarity score.

\- SBERT semantic similarity score.

\- Skill matching score.

\- Matched skills.

\- Missing skills.

\- Explanation summary.

\- Model version and inference latency.



\### 3.6 User Roles



| Role | Main Responsibilities |

|---|---|

| Candidate / User | Resume management, job discovery, matching insights, applications and tracking. |

| Recruiter | Job description creation, candidate screening, ranking, comparison, shortlisting and feedback. |

| Administrator | User and system administration, model information, experiments and monitoring. |



\## 4. System Architecture



ResumeIQ follows a layered architecture.



\### Client Layer

\- React

\- TypeScript

\- Vite

\- Tailwind CSS

\- Responsive Progressive Web Application



\### Application Layer

\- FastAPI

\- REST API

\- Pydantic validation

\- Authentication and authorization

\- File handling and business logic



\### AI / NLP Layer

\- Resume and job-description parsing

\- Text preprocessing

\- Skill extraction

\- TF-IDF similarity

\- SBERT semantic similarity

\- Hybrid matching

\- Candidate ranking

\- Explainability and fairness evaluation



\### Data and MLOps Layer

\- SQLite for development

\- PostgreSQL for deployment

\- Local file storage / AWS S3

\- DVC and DagsHub

\- MLflow

\- Pytest

\- GitHub Actions

\- Docker and Docker Compose

\- Prometheus and Grafana

\- Evidently AI



\### End-to-End Workflow



```text

Candidate Resume + Job Description

&#x20;                |

&#x20;                v

&#x20;        Document Parsing

&#x20;                |

&#x20;                v

&#x20;       NLP Preprocessing

&#x20;                |

&#x20;                v

&#x20;      Information Extraction

&#x20;    (Skills, Education, Experience)

&#x20;                |

&#x20;                v

&#x20;         Feature Generation

&#x20;         /       |       \\

&#x20;        /        |        \\

&#x20;     TF-IDF     SBERT    Skills

&#x20;        \\        |        /

&#x20;         \\       |       /

&#x20;          Hybrid Matching

&#x20;                |

&#x20;                v

&#x20;       Candidate Scoring

&#x20;                |

&#x20;                v

&#x20;      Ranking and Explanation

&#x20;                |

&#x20;                v

&#x20;        FastAPI REST API

&#x20;                |

&#x20;                v

&#x20;      Responsive React PWA

&#x20;                |

&#x20;                v

&#x20;     Monitoring and Feedback

&#x20;                |

&#x20;                v

&#x20;     Evaluation and Retraining

```



\## 5. Technology Stack



| Category | Technologies |

|---|---|

| Programming Language | Python 3.11 |

| Frontend | React, TypeScript, Vite |

| Styling | Tailwind CSS, HTML, CSS |

| Backend | FastAPI, Uvicorn |

| Data Validation | Pydantic |

| NLP and Machine Learning | Scikit-learn, Sentence-Transformers, spaCy, NLTK |

| Numerical Processing | NumPy, Pandas |

| Document Processing | PyMuPDF, python-docx |

| Database | SQLite, PostgreSQL |

| Data Versioning | DVC, DagsHub |

| Experiment Tracking | MLflow |

| Testing | Pytest |

| CI/CD | GitHub Actions |

| Containerization | Docker, Docker Compose |

| Cloud Infrastructure | AWS EC2, AWS S3 |

| Monitoring | Prometheus, Grafana, Evidently AI |

| Version Control | Git and GitHub |

| Development Environment | PyCharm, Python Virtual Environment |



\## 6. Repository Structure



The project follows a modular monorepo structure.



```text

MLOPS-Project-Team-12/

│

├── ai\_nlp/

│   ├── src/

│   │   └── resumeiq\_nlp/

│   │       ├── \_\_init\_\_.py

│   │       └── matching.py

│   ├── tests/

│   │   ├── test\_contract.py

│   │   ├── test\_import.py

│   │   └── test\_matching.py

│   └── pyproject.toml

│

├── backend/

│   ├── app/

│   │   ├── api/

│   │   ├── core/

│   │   ├── schemas/

│   │   ├── services/

│   │   └── main.py

│   ├── tests/

│   ├── requirements.txt

│   └── pytest.ini

│

├── frontend/

│   └── React application files

│

├── contracts/

│   ├── inference\_schema.json

│   ├── example\_match\_result.json

│   ├── example\_parsed\_resume.json

│   ├── example\_parsed\_job.json

│   └── openapi.json

│

├── mlops/

│   ├── experiments/

│   ├── monitoring/

│   └── scripts/

│

├── deploy/

│

├── docs/

│

├── .github/

│   └── workflows/

│

├── .env.example

├── .gitignore

├── requirements-dev.txt

└── README.md

```



\*Note: The structure above summarizes the project modules. Individual files and subdirectories may vary by branch and implementation version.\*



\## 7. Installation and Setup



\### Prerequisites



Install the following software before running the project:



\- Python 3.11

\- Git

\- Node.js and npm (for the frontend)

\- PyCharm or Visual Studio Code

\- Docker Desktop (for containerized execution)



\### Step 1: Clone the Repository



```bash

git clone https://github.com/Yosritha28/MLOPS-Project-Team-12.git

cd MLOPS-Project-Team-12

```



\### Step 2: Create a Virtual Environment



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.venv\\Scripts\\Activate.ps1

```



\### Step 3: Install Dependencies



Install the development requirements:



```bash

python -m pip install -r requirements-dev.txt

```



Install the NLP package in editable mode:



```bash

python -m pip install -e ./ai\_nlp

```



\### Step 4: Configure Environment Variables



Use the example environment file as a reference.



```bash

copy .env.example .env

```



Configure the required environment variables for the local environment.



Do not commit passwords, API keys, secret keys or other sensitive credentials to GitHub.



\## 8. Running the Backend



From the project root:



```powershell

cd backend

```



Enable the SBERT inference option when the semantic model is available:



```powershell

$env:RESUMEIQ\_SBERT = "1"

```



Start the FastAPI application:



```bash

uvicorn app.main:app --reload

```



The backend runs locally at:



```text

http://127.0.0.1:8000

```



FastAPI interactive API documentation:



```text

http://127.0.0.1:8000/docs

```



The interactive documentation can be used to inspect available endpoints and test API requests.



\## 9. Running the Frontend



Open a separate terminal and navigate to the frontend directory:



```bash

cd frontend

```



Install frontend dependencies:



```bash

npm install

```



Start the Vite development server:



```bash

npm run dev

```



Use the local URL printed by Vite in the terminal.



The frontend and backend should be configured to communicate through the appropriate API base URL.



\## 10. MLOps Workflow



ResumeIQ incorporates MLOps practices to improve reproducibility, traceability and maintainability.



\### 10.1 Version Control



Git and GitHub are used for:



\- Source-code versioning.

\- Feature branches.

\- Team collaboration.

\- Pull requests and code integration.



\### 10.2 Data and Pipeline Versioning



DVC and DagsHub support versioning of datasets and ML pipeline artifacts, allowing experiments to be associated with reproducible inputs.



\### 10.3 Experiment Tracking with MLflow



MLflow records experiment runs, model parameters, metrics and related artifacts.



The ResumeIQ matching experiment is named:



```text

resumeiq-matching

```



Example parameters:



```text

w\_tfidf

w\_sbert

w\_skills

```



Example evaluation metrics:



```text

roc\_auc

mrr

top1\_accuracy

```



The MLflow interface can be launched with:



```bash

mlflow ui

```



Open:



```text

http://127.0.0.1:5000

```



Select the `resumeiq-matching` experiment to inspect recorded runs and compare matching configurations.



\### 10.4 Automated Testing



Pytest is used to validate:



\- NLP package imports.

\- Inference contract compatibility.

\- Score boundaries.

\- Matching weight validation.

\- Matching output structure.

\- API behavior.



Run the AI/NLP tests:



```bash

python -m pytest ai\_nlp/tests -v

```



Run backend tests:



```bash

python -m pytest backend/tests -c backend/pytest.ini -v

```



\### 10.5 CI/CD



GitHub Actions supports automated validation and build workflows when changes are pushed to the repository or submitted through pull requests.



\### 10.6 Containerization



Docker and Docker Compose are used to package and coordinate application services for consistent execution across environments.



\### 10.7 Monitoring



The architecture includes:



\- Prometheus for metrics collection.

\- Grafana for monitoring dashboards.

\- Evidently AI for data-quality and drift analysis.



Monitoring results can help identify changes in incoming data and support controlled model evaluation and retraining.



\## 11. Model Evaluation



ResumeIQ compares three matching approaches:



1\. TF-IDF-based lexical matching.

2\. SBERT-based semantic matching.

3\. Hybrid matching using lexical, semantic and skill-based components.



The evaluation process considers:



| Metric | Purpose |

|---|---|

| ROC-AUC | Measures the model's ability to distinguish relevant and non-relevant pairs. |

| MRR | Evaluates the ranking position of the first relevant result. |

| Top-1 Accuracy | Measures whether the first-ranked result is relevant. |

| Latency | Measures the time required to produce matching results. |



MLflow stores the parameters and metrics for each experiment, making it possible to compare model configurations and track changes over time.



Actual evaluation values should be read from the corresponding MLflow runs rather than assumed from example data.



\## 12. API and Inference Contract



The backend exposes REST endpoints through FastAPI.



The project maintains shared inference contracts under the `contracts/` directory.



Important files include:



\- `inference\_schema.json`

\- `example\_match\_result.json`

\- `example\_parsed\_resume.json`

\- `example\_parsed\_job.json`

\- `openapi.json`



The inference contract defines the expected structure of matching results, including:



\- Overall score.

\- Component scores.

\- Component weights.

\- Matched and missing skills.

\- Explanation.

\- Model version.

\- Inference latency.

\- Warnings and optional additional information.



These contracts help maintain consistency between the NLP package, backend services and other project modules.



\## 13. Team Contributions



The project is divided into four technical workstreams.



| Team Member | Workstream | Responsibility |

|---|---|---|

| Yosritha | Member 1 – AI/NLP | Resume parsing, NLP processing, TF-IDF, SBERT and hybrid matching. |

| Dhathri | Member 2 – MLOps | Data versioning, MLflow, testing, CI/CD, Docker and monitoring. |

| Vaishnavi | Member 3 – Backend \& Database | FastAPI services, API contracts, authentication and persistence. |

| Venkata Sravani | Member 4 – Frontend | Responsive React PWA, user interfaces and backend integration. |



\## 14. Future Enhancements



Potential future improvements include:



\- Improved parsing of complex resume layouts and scanned documents.

\- Expanded skill taxonomies and domain-specific extraction.

\- Optimization of semantic inference latency.

\- Larger and more representative evaluation datasets.

\- More extensive fairness evaluation.

\- Improved monitoring and alerting.

\- Controlled feedback-driven retraining.

\- Scalability improvements for cloud deployment.

\- Enhanced multilingual resume processing.

\- Further accessibility and mobile usability improvements.



\## 15. Conclusion



ResumeIQ demonstrates how Natural Language Processing, Machine Learning and MLOps can be integrated to support intelligent resume screening and job matching.



By combining TF-IDF, Sentence-BERT and skill-based matching, the platform evaluates both lexical and semantic relationships between candidate profiles and job requirements.



Its explainable output helps recruiters understand candidate-job compatibility, while candidates can identify relevant strengths and missing skills.



The responsive PWA architecture provides access through desktop and mobile browsers. The MLOps workflow supports reproducibility through versioning, experiment tracking, automated testing, CI/CD, containerization and monitoring.



Overall, ResumeIQ provides a structured foundation for efficient, explainable and continuously improvable recruitment screening.



\## 16. Repository Information



\*\*Project Name:\*\* ResumeIQ – AI-Powered Resume Analysis and Job Matching Platform



\*\*Repository:\*\* \[MLOPS-Project-Team-12](https://github.com/Yosritha28/MLOPS-Project-Team-12)



\*\*Development Language:\*\* Python 3.11



\*\*Project Type:\*\* Machine Learning Operations / AI / NLP / Web Application



\*\*Course:\*\* Machine Learning Operations (24SDAD03)



\*\*Institution:\*\* KLEF – Deemed to be University



\---



<p align="center">

&#x20; <strong>ResumeIQ – AI | Explainable | Fair | MLOps | Web + Mobile PWA</strong>

</p>

