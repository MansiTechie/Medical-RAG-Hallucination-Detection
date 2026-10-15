<div align="center">

# 🩺 Medical RAG — Hallucination Detection System

### Evidence-grounded Medical AI Assistant with Retrieval, Verification, Confidence Scoring & Self-Correction.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge)](https://www.langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-0467DF?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-Embeddings-FF6F00?style=for-the-badge)](https://www.sbert.net/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Gemini](https://img.shields.io/badge/Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

</div>

---

## 🩺 Overview

**Medical RAG Hallucination Detection** is a Retrieval-Augmented Generation (RAG) based Medical AI Assistant designed to generate answers from trusted medical documents while checking whether the generated response is sufficiently supported by the retrieved evidence.

The system combines:

- Medical document retrieval
- Grounded LLM answer generation
- Evidence-based claim verification
- Hallucination detection
- Confidence scoring
- Self-correction

The core idea is:

> **Retrieve → Generate → Verify → Score → Correct → Respond**

The current prototype uses a trusted medical guideline PDF related to diabetes as its primary knowledge source.

---

## 🎯 Project Objective

The goal of this project is to build a medical AI assistant that:

- Answers questions using trusted medical documents.
- Grounds generated responses in retrieved evidence.
- Detects potentially unsupported or contradictory claims.
- Calculates a confidence score for generated answers.
- Performs self-correction when an answer is unreliable.
- Provides source and page-level evidence for verification.

The system is designed to reduce the risk of hallucinated medical information by making retrieved evidence an explicit part of the answer-generation and verification pipeline.

---

## 👥 Team

- **Vivek**
- **Mansi**

### Work Division

**Vivek**
- Dataset collection and preparation
- Trusted source-document organization
- Dataset management
- Overall pipeline review
- Documentation
- Integration
- Final testing

**Mansi**
- LLM integration
- Hallucination detection
- Confidence scoring
- Self-correction
- Backend and integration coding



---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini API |
| RAG Framework | LangChain |
| Embeddings | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | FAISS |
| PDF Processing | PyMuPDF |
| Hallucination Detection | NLI + Semantic Similarity |
| NLI Model | `cross-encoder/nli-deberta-v3-base` |
| Backend | FastAPI |
| Frontend | React |
| Styling | Tailwind CSS |
| Development | VS Code |
| Experimentation | Google Colab |
| Version Control | Git & GitHub |

---

# 📁 Project Structure

```text
Medical-RAG-Hallucination-Detection/
│
├── assets/
│
├── backend/
│
├── dataset/
│   ├── raw/
│   │   └── niddk_guiding_principles_diabetes.pdf
│   └── .gitkeep
│
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── ROADMAP.md
│   ├── TEAM_GUIDELINES.md
│   └── TEAM_HANDOFF.md
│
├── frontend/
│
├── models/
│
├── notebooks/
│   ├── Notebook_01_Project_Setup.ipynb
│   ├── Notebook_02_Environment_Setup.ipynb
│   ├── Notebook_03_PDF_Text_Extraction.ipynb
│   ├── Notebook_04_LLM_Integration.ipynb
│   ├── Notebook_05_Hallucination_Detection.ipynb
│   ├── Notebook_06_Confidence_Scoring.ipynb
│   ├── Notebook_07_Self_Correction.ipynb
│   └── Notebook_08_Pipeline_Integration.ipynb
│
├── outputs/
├── presentation/
├── research/
├── screenshots/
├── scripts/
├── tests/
├── vector_db/
│
├── .gitignore
├── LICENSE
└── README.md
📓 Notebook Development Status

The experimental and model-development phase has been completed through Notebook 08.

Notebook 01 — Project Setup

notebooks/Notebook_01_Project_Setup.ipynb

Handles initial project setup and repository verification.

Status

✅ Completed

Notebook 02 — Environment Setup

notebooks/Notebook_02_Environment_Setup.ipynb

Prepares and verifies the Python/ML development environment.

Status

✅ Completed

Notebook 03 — PDF Text Extraction & FAISS Retrieval

notebooks/Notebook_03_PDF_Text_Extraction.ipynb

Implements the document processing and retrieval foundation.

Workflow
Medical PDF
     ↓
PDF Text Extraction
     ↓
Text Cleaning
     ↓
Text Chunking
     ↓
Sentence Embeddings
     ↓
FAISS Vector Index
     ↓
Similarity Retrieval
Status

✅ PDF loading
✅ Text extraction
✅ Text cleaning
✅ Text chunking
✅ Embedding generation
✅ FAISS indexing
✅ Similarity retrieval

Current Source Document
dataset/raw/niddk_guiding_principles_diabetes.pdf
Document Information
Type: Medical diabetes guideline
Pages: 83
Chunk size: 1000 characters
Chunk overlap: 200 characters
Embedding dimension: 384
Vector database: FAISS
🤖 Notebook 04 — LLM Integration

notebooks/Notebook_04_LLM_Integration.ipynb

Integrates the retrieved medical context with the Gemini LLM.

Workflow
User Question
      ↓
FAISS Retrieval
      ↓
Relevant Medical Context
      ↓
Grounded Prompt
      ↓
Gemini LLM
      ↓
Evidence-based Answer

The model is instructed to answer using the retrieved medical context rather than relying only on internal knowledge.

The pipeline also supports abstention when sufficient evidence is not available.

Status

✅ Gemini integration
✅ Grounded prompting
✅ Context-based answer generation
✅ Insufficient-evidence handling
✅ Retry handling for temporary API errors

🔍 Notebook 05 — Hallucination Detection

notebooks/Notebook_05_Hallucination_Detection.ipynb

This stage checks whether generated answers are supported by retrieved medical evidence.

Two complementary signals are used:

1. Semantic Similarity

Measures how closely the generated answer is related to retrieved medical documents.

2. Natural Language Inference

The retrieved medical evidence is treated as the premise and the generated statement as the hypothesis.

The NLI model evaluates:

Entailment
Contradiction
Neutrality
Support Score

The initial answer-level verification uses:

Support Score =
0.5 × Semantic Similarity
+
0.5 × NLI Entailment

The claim-level verification stage later uses an NLI-first evidence score.

Detection Categories
SUPPORTED
CONTRADICTED
POTENTIAL HALLUCINATION
Status

✅ Semantic similarity verification
✅ NLI verification
✅ Contradiction detection
✅ Claim-level verification
✅ Hallucination classification

📊 Notebook 06 — Confidence Scoring

notebooks/Notebook_06_Confidence_Scoring.ipynb

The system calculates an overall confidence score using multiple signals.

Confidence Formula
Confidence =
0.30 × Answer Semantic Similarity
+
0.30 × NLI Entailment
+
0.20 × Retrieval Quality
+
0.20 × Claim Consistency
Confidence Levels
≥ 0.80  → HIGH
≥ 0.60  → MEDIUM
< 0.60  → LOW

Confidence is used as an additional signal for deciding whether an answer should be corrected.

Status

✅ Confidence calculation
✅ Retrieval quality calculation
✅ Claim consistency
✅ Confidence bands
✅ Self-correction trigger logic

🔄 Notebook 07 — Self-Correction

notebooks/Notebook_07_Self_Correction.ipynb

This stage introduces a feedback loop for unreliable answers.

Workflow
Generated Answer
      ↓
Evidence Verification
      ↓
Confidence + Hallucination Decision
      ↓
Reliable?
   ↙       ↘
 YES        NO
  ↓          ↓
Return    Self-Correction
Answer       ↓
          Evidence
          Based
          Revision

The correction process identifies unsupported claims and provides the available evidence to the LLM so that the answer can be revised using only supported information.

Status

✅ Unsupported claim identification
✅ Evidence collection
✅ Correction prompt generation
✅ Self-correction logic
✅ Correction pipeline testing

🔗 Notebook 08 — Pipeline Integration

notebooks/Notebook_08_Pipeline_Integration.ipynb

This is the final notebook of the experimental development phase.

It combines the major components developed in the previous notebooks into one pipeline.

Integrated Workflow
User Question
      ↓
Document Retrieval
      ↓
Medical Context Construction
      ↓
Grounded LLM Generation
      ↓
Claim Extraction
      ↓
Evidence Retrieval
      ↓
NLI Verification
      ↓
Confidence Scoring
      ↓
Hallucination Decision
      ↓
Self-Correction
      ↓
Final Answer
Current Pipeline Components

✅ Retrieval
✅ Context construction
✅ Grounded answer generation
✅ Claim extraction
✅ Claim-level evidence verification
✅ NLI-based verification
✅ Confidence scoring
✅ Hallucination decision
✅ Self-correction trigger
✅ Integrated pipeline function

Current Validation

The integrated pipeline was tested using diabetes-related medical questions.

The verification pipeline successfully demonstrated:

Evidence retrieval
Supported claim detection
Unsupported claim detection
Confidence calculation
Hallucination classification
Self-correction logic

The final end-to-end Gemini generation test may be limited by external Gemini API quota availability during development.

🧠 Current RAG Architecture
                ┌──────────────────┐
                │   User Question  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │  FAISS Retrieval │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Medical Context  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │   Gemini LLM     │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Generated Answer │
                └────────┬─────────┘
                         ↓
              ┌──────────────────────┐
              │ Claim Verification   │
              │ Semantic + NLI       │
              └──────────┬───────────┘
                         ↓
              ┌──────────────────────┐
              │ Confidence Scoring   │
              └──────────┬───────────┘
                         ↓
              ┌──────────────────────┐
              │ Hallucination Check  │
              └──────────┬───────────┘
                         ↓
                  ┌──────────────┐
                  │ Self-Correct?│
                  └──────┬───────┘
                     YES │ NO
                         ↓
                ┌──────────────────┐
                │   Final Answer   │
                └──────────────────┘
📚 Dataset

The current prototype uses a trusted medical guideline document related to diabetes.

Current Source
dataset/raw/niddk_guiding_principles_diabetes.pdf
Document

NIDDK Guiding Principles for the Care of People With or at Risk for Diabetes

The document is processed through:

PDF
 ↓
Extraction
 ↓
Cleaning
 ↓
Chunking
 ↓
Embedding
 ↓
FAISS Index
 ↓
Retrieval

The project is currently based on public medical guideline material and does not use private patient data.

📌 Evidence Grounding

A central design principle of the system is that medical answers should be grounded in retrieved evidence.

Each retrieved chunk contains metadata such as:

Chunk ID
Page number
Source document
Retrieved text
Similarity information

This allows generated claims to be compared against specific medical evidence.

🧪 Testing & Evaluation

Testing is performed progressively throughout development.

Current testing areas include:

PDF processing
Retrieval relevance
Grounded answer generation
Semantic similarity
NLI verification
Claim-level verification
Hallucination detection
Confidence scoring
Self-correction
Integrated pipeline behavior

Future testing will focus on:

End-to-end API testing
Frontend interaction testing
Backend/frontend integration
Response consistency
Failure handling
Final system evaluation
🚀 Current Development Status
[✓] Project Setup
       ↓
[✓] Environment Setup
       ↓
[✓] Medical PDF Added
       ↓
[✓] PDF Text Extraction
       ↓
[✓] Text Cleaning
       ↓
[✓] Text Chunking
       ↓
[✓] Embedding Generation
       ↓
[✓] FAISS Retrieval
       ↓
[✓] LLM Integration
       ↓
[✓] Grounded Answer Generation
       ↓
[✓] Hallucination Detection
       ↓
[✓] Confidence Scoring
       ↓
[✓] Self-Correction
       ↓
[✓] Pipeline Integration
       ↓
[ ] FastAPI Backend
       ↓
[ ] React Frontend
       ↓
[ ] Backend ↔ Frontend Integration
       ↓
[ ] Final Testing & Evaluation
Current Milestone

Experimental RAG + Hallucination Detection Pipeline Completed Through Notebook 08

Next Milestone

FastAPI Backend Development in VS Code

The notebook/Colab development phase is now considered complete for the current implementation.

💻 Development Workflow

The project initially used Google Colab for experimentation and model/pipeline development.

The development workflow now moves to VS Code for the remaining implementation.

Completed Experimental Phase
          ↓
     Notebooks 01–08
          ↓
      VS Code
          ↓
    FastAPI Backend
          ↓
    React Frontend
          ↓
 Backend + Frontend
     Integration
          ↓
 Final Testing
🔐 Security

API keys and secrets must never be committed to GitHub.

Never write:

API_KEY = "actual-secret-key"

Use environment variables or secure secret management instead.

Never commit:

.env
API keys
Passwords
Access tokens
Private credentials
⚠️ Medical Disclaimer

This project is intended for educational and research purposes only.

It is not a replacement for professional medical advice, diagnosis, or treatment.

The system is designed to retrieve information from trusted medical sources and demonstrate techniques for improving the grounding and reliability of AI-generated medical responses.

Users should consult qualified healthcare professionals for medical decisions.

🔮 Future Scope

Planned future improvements include:

FastAPI backend integration
REST API for the RAG pipeline
React-based medical assistant interface
PDF upload and document processing
Source/page citations in the UI
Confidence visualization
Hallucination warnings
Self-correction display
Multi-document medical knowledge base
Additional trusted medical sources
Improved evaluation datasets
Robust end-to-end testing
🤝 Git & GitHub Workflow

Before starting work:

git pull --rebase origin main

After completing a meaningful change:

git status
git add <changed-files>
git commit -m "Describe the change"
git pull --rebase origin main
git push origin main

Never use:

git push -f

If a merge or rebase conflict occurs, coordinate before resolving it.

📌 Project Status

Current Status:

🟢 RAG experimentation and pipeline development completed through Notebook 08

Completed:

Medical PDF processing
FAISS retrieval
Gemini grounded generation
Hallucination detection
NLI claim verification
Confidence scoring
Self-correction
Integrated pipeline

Next:

⚙️ FastAPI Backend Development

<div align="center">
🩺 Medical RAG Hallucination Detection

Retrieve → Generate → Verify → Score → Correct

Built with Python, LangChain, FAISS, Sentence Transformers, FastAPI, React & Gemini.

</div> ```