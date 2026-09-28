Yes. For **Q-MedAI**, I recommend making the SRS much more formal than a normal project proposal. It should define exactly **what the system must do, how the React frontend communicates with Python, how the QSVC pipeline is used, what is in scope, what is not, and how the final system will be tested**.

I have also grounded the ML-specific requirements in your uploaded QSVC implementation. Your current pipeline uses three diseases—**Migraine, Common Cold, and Urinary Tract Infection**—with TF-IDF, StandardScaler, PCA to four quantum features/qubits, MinMax angle scaling, a shallow `ZZFeatureMap`, and QSVC with cross-validated `C` tuning. 

# Software Requirements Specification (SRS)

## Q-MedAI — Quantum-Powered Medical Symptom Analyzer

**Document Version:** 1.0
**Document Type:** Software Requirements Specification
**Project Type:** AI / Quantum Machine Learning Web Application
**Frontend:** React.js + Tailwind CSS
**Backend:** Python + FastAPI
**Machine Learning:** Qiskit Quantum Support Vector Classifier (QSVC)
**Architecture:** Clean Architecture / Layered Architecture
**Database:** Optional for Phase 1; PostgreSQL recommended for production
**Primary Interface:** Responsive Web Application
**Target Platforms:** Desktop, Tablet, Mobile
**Document Status:** Initial Production SRS

---

# 1. Introduction

## 1.1 Purpose

The purpose of this Software Requirements Specification is to define the functional, non-functional, technical, architectural, security, usability, and deployment requirements for **Q-MedAI**, a web-based AI-powered medical symptom analysis system.

Q-MedAI will allow a user to describe their symptoms using natural language through a modern web interface. The system will process the submitted symptom description through a pre-trained machine-learning pipeline and return a **preliminary model prediction**.

The system is intended to demonstrate the integration of:

* Natural Language Processing
* Classical machine-learning preprocessing
* Quantum Machine Learning
* Quantum Support Vector Classification
* REST APIs
* React-based frontend development
* FastAPI backend development
* Clean software architecture

Q-MedAI is an **informational and research-oriented symptom analysis system** and shall not represent its prediction as a confirmed medical diagnosis.

---

# 2. Project Overview

## 2.1 Product Name

**Q-MedAI**

### Full Name

**Quantum-Powered Medical Symptom Analyzer**

---

## 2.2 Product Vision

Q-MedAI aims to provide a modern interface through which users can describe health symptoms in natural language and receive a fast, understandable, AI-generated preliminary prediction.

The application combines conventional NLP preprocessing with a quantum machine-learning classification pipeline.

The current ML implementation specifically selects three disease classes:

1. Migraine
2. Common Cold
3. Urinary Tract Infection

The training implementation balances the selected classes and uses a configurable sample count per class. 

---

# 3. Scope

## 3.1 In Scope

The initial production version shall include:

### Frontend

* Premium responsive landing page
* Navigation
* Hero section
* Symptom input interface
* Natural-language textarea
* Character counter
* Analyze button
* Loading state
* Error state
* Prediction result card
* Medical disclaimer
* Technology section
* Responsive design
* Accessibility support
* Mobile navigation
* API integration

### Backend

* FastAPI REST API
* Health-check endpoint
* Prediction endpoint
* Request validation
* Response validation
* CORS configuration
* Error handling
* ML pipeline loading
* Prediction service
* Logging
* Configuration management

### Machine Learning

The system shall load the pre-trained Q-MedAI pipeline and execute:

```text
User Symptom Text
       ↓
TF-IDF
       ↓
StandardScaler
       ↓
PCA
       ↓
Angle Scaling
       ↓
Quantum Kernel / QSVC
       ↓
Label Encoder
       ↓
Disease Prediction
```

The current implementation uses 40 TF-IDF features before PCA and reduces the representation to four dimensions corresponding to the configured number of quantum features/qubits. 

---

# 4. Out of Scope

The following shall **not** be treated as confirmed functionality of Version 1:

* Medical diagnosis
* Prescription generation
* Medication recommendations
* Emergency treatment
* Automated doctor replacement
* Medical image diagnosis
* Blood-test interpretation
* Electronic health records
* Hospital management
* Insurance processing
* Online consultation
* Emergency dispatch
* Autonomous medical decision-making

These may be considered future extensions.

---

# 5. Intended Users

## 5.1 General User

A person who wants to enter symptoms and receive preliminary informational analysis.

## 5.2 Healthcare / Research User

A researcher, student, developer, or healthcare technology professional interested in evaluating the system's AI/quantum classification pipeline.

## 5.3 System Administrator

An authorized technical administrator responsible for:

* Application configuration
* Model deployment
* System monitoring
* API configuration
* Model version management

---

# 6. System Objectives

The system shall:

1. Provide an intuitive symptom-entry experience.
2. Accept natural-language symptom descriptions.
3. Validate user input.
4. Send the request securely to the FastAPI backend.
5. Process the text through the trained Q-MedAI pipeline.
6. Return the predicted disease class.
7. Display the result clearly.
8. Clearly distinguish prediction from medical diagnosis.
9. Handle backend/model failures gracefully.
10. Provide a scalable architecture for future ML models and additional diseases.

---

# 7. System Architecture

The recommended architecture is:

```text
                         Q-MedAI
                            │
             ┌──────────────┴──────────────┐
             │                             │
        React Frontend                FastAPI Backend
             │                             │
        Tailwind CSS                  API Layer
             │                             │
       Component Layer              Application Layer
             │                             │
        API Service                  Prediction Service
             │                             │
             └──────────────┬──────────────┘
                            │
                     ML Pipeline Layer
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Preprocessing              Quantum Model
              │                           │
       TF-IDF → Scaler              QSVC / Kernel
              ↓                           │
             PCA                          │
              ↓                           │
       Angle Scaling ─────────────────────┘
                            │
                      Label Encoder
                            │
                     Prediction Result
```

---

# 8. Recommended Project Structure

The production project shall use the following structure:

```text
Q-MedAI/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   │
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   └── prediction.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── prediction.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── prediction_service.py
│   │   │
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── model_loader.py
│   │   │   ├── preprocessing.py
│   │   │   └── predictor.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py
│   │
│   ├── models/
│   │   └── q_medai_pipeline.dill
│   │
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_prediction.py
│   │   ├── test_validation.py
│   │   └── test_model.py
│   │
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   │
│   ├── public/
│   │   ├── favicon.svg
│   │   └── logo.svg
│   │
│   ├── src/
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Footer.jsx
│   │   │   │
│   │   │   ├── hero/
│   │   │   │   └── Hero.jsx
│   │   │   │
│   │   │   ├── analyzer/
│   │   │   │   ├── SymptomInput.jsx
│   │   │   │   ├── AnalyzeButton.jsx
│   │   │   │   ├── LoadingState.jsx
│   │   │   │   ├── ResultCard.jsx
│   │   │   │   └── Disclaimer.jsx
│   │   │   │
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Card.jsx
│   │   │       └── Toast.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── NotFound.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── hooks/
│   │   │   └── usePrediction.js
│   │   │
│   │   ├── utils/
│   │   │   └── constants.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── vite.config.js
│   ├── .env
│   └── .env.example
│
├── docs/
│   ├── SRS.md
│   ├── API.md
│   └── ARCHITECTURE.md
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

# 9. Functional Requirements

## FR-001 — Application Loading

The system shall load the Q-MedAI web application when the user visits the frontend URL.

The application shall display:

* Q-MedAI branding
* Navigation
* Hero section
* Symptom analyzer
* Technology information
* Medical disclaimer
* Footer

---

# 10. User Registration

### Version 1

User registration shall **not be mandatory**.

A user shall be able to perform a symptom analysis without creating an account.

### Future Version

The system may support:

* Account creation
* Login
* Saved assessments
* Assessment history
* User profile

---

# 11. Symptom Input Requirements

## FR-002 — Symptom Text Input

The system shall provide a large textarea for entering symptoms.

The user may enter free-form natural-language text.

Example:

```text
I have had a severe headache for two days.
I also feel nauseous and sensitive to bright light.
```

---

## FR-003 — Input Validation

The frontend shall reject:

* Empty input
* Whitespace-only input
* Extremely short descriptions
* Input exceeding the configured maximum length

Recommended maximum:

```text
5000 characters
```

The backend shall perform the same validation independently.

Frontend validation shall **never replace backend validation**.

---

# 12. Prediction Request

The frontend shall send:

```http
POST /predict
```

with:

```json
{
  "symptoms": "I have a severe headache..."
}
```

Content type:

```http
Content-Type: application/json
```

---

# 13. Prediction Processing

The backend shall retrieve the following components from the serialized model pipeline:

```text
model
tfidf
scaler
pca
angle_scaler
label_encoder
```

The uploaded training implementation explicitly defines the corresponding preprocessing components and label encoder. 

The inference sequence shall be:

```text
Input Text
    ↓
TF-IDF Transformation
    ↓
Scaler Transformation
    ↓
PCA Transformation
    ↓
Angle Scaling
    ↓
QSVC Prediction
    ↓
Label Decoding
```

The system shall not independently refit any preprocessing component during prediction.

---

# 14. Quantum Machine Learning Requirements

The current model uses:

```text
Algorithm: QSVC
Kernel: FidelityQuantumKernel
Feature Map: ZZFeatureMap
Feature Map Repetitions: 1
Quantum Features/Qubits: 4
```

These parameters are defined by the current implementation. 

The production API shall treat the trained pipeline as an inference artifact.

It shall **not train the model during a normal `/predict` request**.

---

# 15. Model Loading

At application startup, the backend shall load:

```text
models/q_medai_pipeline.dill
```

The model shall be loaded once and retained in application memory where practical.

The backend shall validate that the pipeline contains:

```text
model
tfidf
scaler
pca
angle_scaler
label_encoder
```

If any required component is missing, the application shall report a model initialization failure.

---

# 16. Prediction Response

Successful response:

```json
{
  "success": true,
  "prediction": "Migraine"
}
```

The API should eventually be extensible to:

```json
{
  "success": true,
  "prediction": {
    "disease": "Migraine",
    "confidence": null,
    "model_version": "q-medai-v1"
  }
}
```

However, **confidence must not be fabricated** if the underlying QSVC pipeline does not provide a calibrated and meaningful probability.

---

# 17. Health Check

The backend shall expose:

```http
GET /health
```

Example:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "Q-MedAI"
}
```

This endpoint shall be used by:

* Frontend diagnostics
* Docker health checks
* Deployment monitoring
* System administrators

---

# 18. Error Handling

The system shall handle:

### HTTP 400

Invalid request.

Example:

```json
{
  "detail": "Please provide your symptoms."
}
```

### HTTP 422

Invalid request schema.

### HTTP 503

ML model unavailable.

### HTTP 500

Unexpected prediction failure.

The frontend shall convert these responses into user-friendly messages.

The application shall never expose:

* Python stack traces
* File-system paths
* Internal model details
* Secret keys
* Environment variables

to normal end users.

---

# 19. Frontend UI/UX Requirements

The frontend shall follow a **premium clinical technology aesthetic**.

## Design references

The visual language should combine:

* Apple Health
* Apple-style minimalism
* Linear
* Vercel
* Modern medical SaaS
* Premium AI interfaces

---

# 20. Color System

Primary:

```text
Healthcare Blue
#2563EB
```

Secondary:

```text
Medical Cyan
#06B6D4
```

Accent:

```text
Teal
#0D9488
```

Background:

```text
#F8FAFC
```

Primary text:

```text
#0F172A
```

Secondary text:

```text
#64748B
```

Success:

```text
#10B981
```

Warning:

```text
#F59E0B
```

Error:

```text
#EF4444
```

The design shall avoid excessive use of saturated colors.

---

# 21. Typography

Recommended font:

```text
Inter
```

Fallback:

```text
system-ui
-apple-system
BlinkMacSystemFont
Segoe UI
sans-serif
```

Typography shall use:

* Strong hierarchy
* Large hero heading
* Medium-weight body text
* Compact metadata
* High readability

---

# 22. Hero Section

The hero section shall include:

### Eyebrow

```text
Quantum-enhanced healthcare intelligence
```

### Main heading

Concept:

> Understand your symptoms. Explore what they may indicate.

### Supporting text

Explain:

* Natural-language symptom analysis
* AI/quantum technology
* Preliminary nature of prediction

### Trust indicators

Examples:

```text
Quantum ML
Privacy Focused
Fast Analysis
Research Driven
```

---

# 23. Symptom Analyzer

The analyzer is the application's primary interaction.

It shall include:

### Header

```text
AI Symptom Assessment
```

### Description

```text
Describe what you're experiencing in your own words.
```

### Textarea

Requirements:

* Large
* Responsive
* Rounded corners
* Focus ring
* Smooth transitions
* Character counter
* Accessible label
* Placeholder example

---

# 24. Analyze Button

The primary CTA shall say:

```text
Analyze Symptoms
```

During processing:

```text
Analyzing your symptoms...
```

The button shall:

* Disable during request
* Display spinner
* Prevent duplicate requests
* Restore normal state after completion

---

# 25. Loading State

The UI shall not appear frozen.

While the backend is processing, display:

```text
Analyzing your symptoms
Processing your symptom profile...
```

A skeleton/shimmer state may be displayed.

The loading animation should remain subtle and professional.

---

# 26. Result Card

The result card shall appear after a successful prediction.

Example:

```text
✓ Analysis Complete

Preliminary Prediction

Migraine
```

The card shall use:

* Smooth fade/slide animation
* Medical icon
* Clear typography
* White surface
* Soft shadow
* Accent border
* Accessible contrast

---

# 27. Medical Disclaimer

The result screen shall prominently display:

> This result is an AI-generated preliminary prediction based on the symptoms provided. It is not a medical diagnosis and should not replace evaluation by a qualified healthcare professional.

The application shall not imply certainty beyond what the model actually establishes.

---

# 28. Accessibility Requirements

The application shall follow WCAG-oriented accessibility principles.

Requirements include:

* Keyboard navigation
* Visible focus states
* Semantic HTML
* Accessible form labels
* Sufficient color contrast
* ARIA labels where appropriate
* Screen-reader-friendly error messages
* No information conveyed solely through color

---

# 29. Responsive Design

The application shall support:

```text
Mobile
Tablet
Laptop
Desktop
Large Desktop
```

Recommended breakpoints:

```text
sm
md
lg
xl
2xl
```

The primary analyzer shall remain usable on screens as narrow as approximately 320px.

---

# 30. API Architecture

The API shall follow:

```text
HTTP
 ↓
Router
 ↓
Schema Validation
 ↓
Application Service
 ↓
ML Service
 ↓
Prediction
 ↓
Response Schema
```

Routes shall not directly contain complex ML logic.

For example:

```text
routes/prediction.py
        ↓
services/prediction_service.py
        ↓
ml/predictor.py
```

This separation is required for maintainability and testing.

---

# 31. Clean Architecture Requirements

The system shall maintain separation of concerns.

## Presentation Layer

Responsible for:

* HTTP
* React components
* User interaction
* API communication

## Application Layer

Responsible for:

* Prediction use cases
* Business orchestration

## Domain Layer

Responsible for:

* Core prediction concepts
* Domain models
* Business rules

## Infrastructure Layer

Responsible for:

* Dill
* Qiskit
* Scikit-learn
* File system
* External services

---

# 32. Security Requirements

## SEC-001 — Secrets

Secrets shall never be hardcoded.

Use:

```text
.env
```

and environment variables.

---

## SEC-002 — CORS

CORS shall only permit known frontend origins in production.

Development:

```text
http://localhost:5173
```

Production:

```text
https://your-domain.com
```

Wildcard CORS should not be used in production unless there is a documented reason.

---

## SEC-003 — Input Sanitization

User input shall be validated before processing.

The system shall enforce:

* Length limits
* Data type validation
* Empty-input rejection

---

## SEC-004 — Error Leakage

Internal exceptions shall be logged server-side but sanitized before being returned to clients.

---

# 33. Privacy Requirements

Because symptom descriptions can contain sensitive health information, the system shall treat submitted symptom text as potentially sensitive.

Version 1 should:

* Avoid unnecessary storage
* Avoid logging raw symptom descriptions
* Avoid exposing submitted symptoms in URLs
* Avoid storing symptoms in browser local storage unless explicitly required
* Avoid sending symptom data to unrelated third-party services

If persistence is introduced later, the system shall define:

* Data retention period
* Encryption requirements
* Access controls
* User deletion mechanism
* Audit logging

---

# 34. Performance Requirements

## Backend

Normal API processing should target:

```text
< 5 seconds
```

for a typical prediction request under normal system conditions.

Quantum kernel computation may cause higher latency depending on the environment.

The frontend shall remain responsive while waiting.

---

# 35. Scalability

The architecture shall allow future support for:

```text
3 diseases
       ↓
10 diseases
       ↓
50+ diseases
       ↓
Expanded classification system
```

The frontend shall not hardcode individual disease names.

Disease classes should come from the backend/model configuration.

---

# 36. Model Performance Requirements

The system shall record:

* Training accuracy
* Test accuracy
* Cross-validation mean
* Cross-validation standard deviation
* Precision
* Recall
* F1-score
* Generalization gap

The current training implementation already calculates these metrics. 

The model training pipeline also evaluates the confusion matrix and classification report. 

---

# 37. Model Quality Requirements

The production system shall not determine model quality using training accuracy alone.

The evaluation process shall consider:

```text
Training Accuracy
        +
Test Accuracy
        +
Cross-Validation
        +
CV Standard Deviation
        +
Precision
        +
Recall
        +
F1
        +
Generalization Gap
```

The current training code specifically calculates the difference between training accuracy and CV performance as a generalization check. 

---

# 38. Dataset Requirements

The current training pipeline expects:

```text
symptom-disease-train-dataset.csv
symptom-disease-test-dataset.csv
mapping.json
```

The expected dataset contains at minimum:

```text
text
label
```

The model maps disease names to label identifiers through `mapping.json`. 

---

# 39. Data Preprocessing Requirements

The current preprocessing cleans text by:

* Converting to string
* Replacing underscores with spaces
* Removing non-alphabetic characters
* Normalizing whitespace
* Converting to lowercase

This behavior is explicitly defined in the training implementation. 

**Important production requirement:** inference preprocessing must remain compatible with the preprocessing used during model training.

---

# 40. ML Configuration

Current configuration:

| Parameter        |        Value |
| ---------------- | -----------: |
| Diseases         |            3 |
| Samples/Class    |    60 target |
| TF-IDF Features  |           40 |
| PCA Components   |            4 |
| Quantum Qubits   |            4 |
| Feature Map      | ZZFeatureMap |
| Feature Map Reps |            1 |
| Test Size        |          30% |
| CV Folds         |            5 |
| Random State     |           42 |

These values are taken from the current training configuration. 

---

# 41. Model Training Requirements

Model training shall be separated from production inference.

```text
Training Environment
       ↓
Dataset
       ↓
Preprocessing
       ↓
Training
       ↓
Evaluation
       ↓
Validation
       ↓
Serialization
       ↓
q_medai_pipeline.dill
       ↓
Production API
```

The production FastAPI server shall **not train the model automatically**.

---

# 42. Logging Requirements

The backend shall log:

* Application startup
* Model loading
* API request status
* Prediction success/failure
* Application errors
* Shutdown events

The backend shall **not log raw patient symptom descriptions by default**.

---

# 43. Testing Requirements

The project shall contain automated tests.

## Unit Tests

Test:

* Input validation
* Text preprocessing
* Model loading
* Prediction service
* Error handling

## API Tests

Test:

```text
GET /health
POST /predict
```

Test:

* Valid request
* Empty request
* Invalid request
* Oversized request
* Model unavailable
* Internal error

---

# 44. Frontend Testing

The frontend shall test:

* Application rendering
* Input validation
* Loading state
* API success
* API failure
* Result rendering
* Mobile layout
* Keyboard accessibility

---

# 45. Deployment Architecture

Recommended production architecture:

```text
                   Internet
                      │
                      ▼
                HTTPS / Domain
                      │
                      ▼
              Reverse Proxy
             Nginx / Cloudflare
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
     React Frontend          FastAPI API
       Static Build             │
                                ▼
                          Q-MedAI Model
                                │
                                ▼
                    q_medai_pipeline.dill
```

---

# 46. Docker Support

The application should eventually support:

```text
docker-compose.yml
```

with services:

```text
frontend
backend
```

A future production architecture may add:

```text
PostgreSQL
Redis
Nginx
Monitoring
```

---

# 47. Browser Compatibility

The frontend shall support modern versions of:

* Google Chrome
* Microsoft Edge
* Mozilla Firefox
* Safari

---

# 48. Non-Functional Requirements

## NFR-001 — Usability

A first-time user should understand how to perform an assessment without instructions.

## NFR-002 — Reliability

A backend failure shall not crash the frontend.

## NFR-003 — Maintainability

Frontend components and backend services shall be modular.

## NFR-004 — Extensibility

Additional ML models should be integratable without rewriting the entire application.

## NFR-005 — Security

Sensitive information shall not be unnecessarily stored or exposed.

## NFR-006 — Accessibility

Core functionality shall be usable through keyboard navigation and accessible UI patterns.

## NFR-007 — Performance

The UI shall provide immediate visual feedback after user interaction.

## NFR-008 — Observability

Backend failures shall be logged sufficiently for developers to diagnose problems.

---

# 49. User Flow

The primary user journey shall be:

```text
User opens Q-MedAI
        ↓
Views landing page
        ↓
Clicks / scrolls to analyzer
        ↓
Reads instructions
        ↓
Enters symptoms
        ↓
Clicks "Analyze Symptoms"
        ↓
Frontend validates input
        ↓
Loading state appears
        ↓
POST /predict
        ↓
FastAPI validates request
        ↓
Prediction service executes
        ↓
TF-IDF
        ↓
Scaler
        ↓
PCA
        ↓
Angle Scaling
        ↓
QSVC
        ↓
Label Encoder
        ↓
Prediction returned
        ↓
Frontend displays result
        ↓
Medical disclaimer
```

---

# 50. Example API Contract

## Request

```http
POST /predict
```

```json
{
  "symptoms": "I have a severe headache and nausea."
}
```

## Success

```http
200 OK
```

```json
{
  "success": true,
  "prediction": "Migraine"
}
```

## Invalid Input

```http
400 Bad Request
```

```json
{
  "detail": "Please provide your symptoms."
}
```

## Model Unavailable

```http
503 Service Unavailable
```

```json
{
  "detail": "Q-MedAI model is currently unavailable."
}
```

---

# 51. Acceptance Criteria

The project shall be considered functionally complete when:

### Frontend

* [ ] React application runs successfully.
* [ ] Tailwind CSS is configured.
* [ ] Responsive design works.
* [ ] User can enter symptoms.
* [ ] Empty input is rejected.
* [ ] Loading state is displayed.
* [ ] API errors are handled.
* [ ] Prediction result is displayed.
* [ ] Medical disclaimer is visible.
* [ ] UI is keyboard accessible.

### Backend

* [ ] FastAPI starts successfully.
* [ ] Model pipeline loads successfully.
* [ ] `/health` works.
* [ ] `/predict` works.
* [ ] CORS is configured.
* [ ] Invalid requests are rejected.
* [ ] Model errors are handled.
* [ ] Internal stack traces are not exposed.

### ML

* [ ] `q_medai_pipeline.dill` loads.
* [ ] TF-IDF transformation works.
* [ ] Scaler transformation works.
* [ ] PCA transformation works.
* [ ] Angle scaling works.
* [ ] QSVC prediction works.
* [ ] Label decoding works.
* [ ] Prediction is returned through API.

---

# 52. Future Roadmap

The architecture should support future phases.

### Phase 1 — Core MVP

```text
React
+
Tailwind
+
FastAPI
+
QSVC
+
3 diseases
```

### Phase 2 — Expanded Intelligence

```text
More disease classes
+
Improved dataset
+
Model versioning
+
Better evaluation
```

### Phase 3 — Patient Experience

```text
User accounts
+
Assessment history
+
Personal dashboard
+
PDF reports
```

### Phase 4 — Clinical Ecosystem

```text
Doctor recommendations
+
Specialist matching
+
Hospital integration
+
FHIR/health-data integration
```

### Phase 5 — Advanced QML

```text
Multiple quantum models
+
Model comparison
+
Quantum/classical benchmarking
+
Advanced explainability
```

---

# 53. Important Product Boundary

Q-MedAI shall be positioned as:

> **An AI-powered preliminary symptom analysis and research system.**

It shall **not** be positioned as:

> An autonomous medical diagnostic system.

The frontend, API documentation, README, result screen, and future marketing material should consistently maintain this distinction.

---

# 54. Definition of Done

The Q-MedAI web application will be considered production-ready for its defined scope when:

```text
✓ Clean Architecture
✓ React frontend
✓ Tailwind CSS
✓ FastAPI backend
✓ Validated REST API
✓ Serialized QSVC model
✓ Correct preprocessing pipeline
✓ Responsive premium UI
✓ Loading/error/success states
✓ Accessibility
✓ Secure CORS
✓ Environment configuration
✓ Logging
✓ Automated tests
✓ API documentation
✓ Deployment configuration
✓ README
✓ Medical disclaimer
✓ No raw symptom logging
✓ Model-version documentation
```

---

## Recommended final technology stack

| Layer                    | Technology                              |
| ------------------------ | --------------------------------------- |
| Frontend                 | React.js                                |
| Build Tool               | Vite                                    |
| Styling                  | Tailwind CSS                            |
| Icons                    | Lucide React                            |
| HTTP                     | Fetch / Axios                           |
| Backend                  | Python                                  |
| API                      | FastAPI                                 |
| Validation               | Pydantic                                |
| ML Serialization         | Dill                                    |
| NLP                      | Scikit-learn TF-IDF                     |
| Dimensionality Reduction | PCA                                     |
| Quantum ML               | Qiskit Machine Learning                 |
| Classifier               | QSVC                                    |
| Quantum Kernel           | FidelityQuantumKernel                   |
| Feature Map              | ZZFeatureMap                            |
| Database                 | PostgreSQL — future/persistent features |
| Testing Backend          | Pytest                                  |
| Testing Frontend         | Vitest + React Testing Library          |
| Deployment               | Docker + Nginx                          |
| Version Control          | Git/GitHub                              |

### One architectural decision I strongly recommend

Keep **training and inference as two separate systems**. Your current training code performs class balancing, train/test splitting, PCA fitting, angle scaling, GridSearchCV, and evaluation during model development.  The production web application should **only load the already-trained pipeline and perform inference**. This makes the web application faster, safer, reproducible, and much easier to deploy.

This SRS can now serve as the **master specification** for building the actual React + FastAPI Q-MedAI application.
