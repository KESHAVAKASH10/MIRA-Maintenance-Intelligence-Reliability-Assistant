# MIRA – Maintenance Intelligence & Reliability Assistant

> AI-powered Industrial Knowledge Intelligence Platform for Maintenance, Reliability and Compliance.

---

## Overview

MIRA (Maintenance Intelligence & Reliability Assistant) is an AI-powered Retrieval-Augmented Generation (RAG) platform that transforms scattered industrial documentation into an intelligent operational knowledge system.

Instead of manually searching through hundreds of SOPs, manuals, incident reports, work orders, and regulatory documents, maintenance engineers can simply ask questions in natural language and receive accurate, context-aware answers.

MIRA combines semantic search, knowledge graphs, predictive maintenance analytics, compliance intelligence, and equipment-centric insights into one unified platform.

---

# Problem Statement

Industrial organizations maintain thousands of documents including:

- Equipment Manuals
- Standard Operating Procedures
- Incident Reports
- Root Cause Analysis Reports
- Inspection Records
- Work Orders
- Regulatory Standards

Finding relevant information during maintenance or emergency situations is slow, error-prone, and heavily dependent on experienced personnel.

MIRA solves this by creating an AI-powered industrial knowledge assistant capable of understanding documents instead of simply storing them.

---

# Features

## AI Industrial Copilot

- Natural language question answering
- Context-aware responses
- NVIDIA Llama 3.1 70B integration
- Citation-aware answers
- Confidence scoring

---

## Retrieval-Augmented Generation (RAG)

- Semantic document search
- Vector embeddings
- BM25 hybrid retrieval
- Cross-encoder reranking
- Intelligent context builder

---

## Equipment 360

Complete asset intelligence dashboard containing:

- Equipment Summary
- Maintenance History
- Related Documents
- Recommendations
- Knowledge Graph
- Health Summary

---

## Knowledge Graph

Graph-based relationship engine connecting

Equipment

↓

Documents

↓

Incidents

↓

Maintenance

↓

Regulations

Allows engineers to visualize document relationships around every industrial asset.

---

## Predictive Maintenance

Generates

- Health Score
- Risk Score
- Remaining Useful Life
- Maintenance Priority
- Failure Probability
- AI Recommendations

---

## Compliance Intelligence

Automatically evaluates equipment against

- OISD Standards
- Factory Act Regulations
- Audit Documents
- Compliance Reports

Outputs

- Compliance Score
- Audit Findings
- Applicable Regulations

---

## Document Intelligence

Supports

- Equipment Manuals
- SOPs
- Work Orders
- Inspection Reports
- Incident Reports
- RCA Reports
- Regulatory Standards

---

# Architecture

```
                    PDF Documents
                          │
                          ▼
                Document Processing
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  Metadata Extraction   Chunking      Equipment Detection
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                Vector Embedding
      (BAAI/bge-small-en-v1.5)
                          │
                          ▼
                     ChromaDB
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
   Semantic Search                 BM25 Search
          │                               │
          └───────────────┬───────────────┘
                          ▼
                 Cross Encoder Reranker
                          │
                          ▼
                   Context Builder
                          │
                          ▼
            NVIDIA Llama 3.1 70B Instruct
                          │
                          ▼
                   AI Generated Answer
```

---

# Tech Stack

## Backend

- FastAPI
- Python
- ChromaDB
- SentenceTransformers
- NetworkX
- OpenAI SDK
- NVIDIA NIM
- dotenv

---

## AI Models

Embedding

- BAAI/bge-small-en-v1.5

Reranker

- cross-encoder/ms-marco-MiniLM-L-6-v2

LLM

- NVIDIA Llama 3.1 70B Instruct

---

## Frontend

- React
- Vite
- TailwindCSS
- Axios
- React Router

---

# Project Structure

```
MIRA

backend/
│
├── services/
│   ├── predictive/
│   ├── graph/
│   ├── compliance/
│   ├── vector_search.py
│   ├── reranker.py
│   ├── knowledge_engine.py
│   └── chat_service.py
│
├── documents/
├── data/
├── main.py
│
frontend/
│
├── pages/
├── components/
├── services/
├── hooks/
└── assets/
```

---

# API Endpoints

```
GET  /

GET  /health

GET  /stats

POST /ask

POST /upload

GET /equipment/{tag}

GET /graph/equipment/{tag}

GET /graph/stats

GET /predictive/{equipment}

GET /compliance/{equipment}

GET /documents

GET /documents/search/{query}
```

---

# Sample Equipment

- PUMP-P101
- PUMP-P102
- PUMP-P103
- COMP-A201

---

# Future Enhancements

- Real-time IoT sensor integration
- SAP PM integration
- IBM Maximo connector
- Digital Twin visualization
- Live maintenance scheduling
- Multi-language support
- Voice-enabled AI assistant

---


MIRA — Maintenance Intelligence & Reliability Assistant

Built for AI-powered Industrial Knowledge Intelligence.

---

