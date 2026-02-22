# Azure AI Knowledge Assistant ☁️🤖

Ein AI-gestützter Azure Architecture Advisor zur Unterstützung von Cloud Engineers und DevOps-Teams bei Architekturentscheidungen, Deployment-Guidance und Troubleshooting im Azure-Umfeld.

Das Projekt demonstriert praktische Erfahrung in **Cloud Engineering, DevOps-Workflows, Containerisierung und AI-Integration** mit Fokus auf Azure-basierte Szenarien.

> Ziel des Projekts: Aufbau eines Cloud-Engineering-Portfolios für eine Junior-Position im Azure / Cloud / DevOps Umfeld.

---

## 🎯 Projektüberblick

Der Azure AI Knowledge Assistant fungiert als interner Cloud-Engineering-Assistent und hilft bei:

- Azure Architekturentscheidungen
- Deployment-Planung und Best Practices
- Troubleshooting von Cloud-Setups
- Schnelleren Projektstarts im Azure-Umfeld
- Kontextbasierter Beratung über eine Knowledge Base (RAG)

Dabei kombiniert das System Large Language Models mit einer projektinternen Knowledge Base zur fundierten Antwortgenerierung.

---

## 🏗️ Architektur & technische Highlights

- Python-basierte Chatbot-Applikation
- Container-ready Architektur (Docker)
- Azure-Deployment vorbereitet (Container Apps / Web App / ACR Workflow)
- Retrieval Augmented Generation (RAG) über lokale Knowledge Base
- Prompt-Separation zur Wartbarkeit (`/prompts`)
- Modularer Retriever (`retriever.py`)
- GitHub-basierte CI/CD Integration

---

## ⚙️ Tech Stack

### Core Technologien

- Python
- Streamlit (UI Framework)
- OpenAI API (LLM Backend)
- Knowledge Base Retrieval (RAG)

### Cloud / DevOps Fokus

- Docker Containerisierung
- Azure Container Registry (ACR)
- GitHub Actions CI/CD Pipeline
- Azure-ready Deployment Architektur

> Hinweis: Azure OpenAI Integration ist geplant. Aktuell wird die Standard OpenAI API verwendet (Subscription-Limitierungen).

---

## ✨ Features

### 🤖 AI Cloud Advisor

- Architektur-Empfehlungen für Azure Workloads
- Security / Reliability / Cost Trade-offs
- Deployment-Guidance
- Cloud Best Practices

### 📚 Knowledge Base Integration

- Kontextbasierte Antworten über eigene KB (`/kb`)
- Erweiterbare Dokumentationsbasis
- RAG-Workflow implementiert

### ⚙️ DevOps-orientiertes Design

- Container-first Ansatz
- Environment-basierte Konfiguration
- CI/CD Deployment vorbereitet

### 🖥️ Chat Interface

- Streamlit Chat UI
- Beispielprompts integriert
- Architektur-Beratungsszenarien simuliert

---

## 📂 Repository Struktur


.
├── app.py # Hauptanwendung (Streamlit Chatbot)
├── retriever.py # Knowledge Base Retrieval
├── kb/ # Knowledge Base Inhalte
├── prompts/ # Prompt Engineering Files
├── Dockerfile # Container Build Setup
├── requirements.txt
└── .github/workflows # CI/CD Pipelines


---

## 🚀 Lokale Nutzung

### Dependencies installieren

```bash
pip install -r requirements.txt
Environment konfigurieren

.env Datei erstellen:

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
Anwendung starten
streamlit run app.py
🐳 Container Deployment

Image bauen:

docker build -t azure-ai-assistant .

Container starten:

docker run -p 8501:8501 --env-file .env azure-ai-assistant
🔄 CI/CD Workflow (Azure Fokus)

Typischer Deployment Ablauf:

Push ins GitHub Repository

GitHub Actions Build Pipeline

Push in Azure Container Registry

Deployment auf Azure Container App / Web App

Damit werden demonstriert:

Container Lifecycle Verständnis

Cloud Deployment Automatisierung

Azure Registry Integration

DevOps Best Practices

🧪 Projektstatus

Aktuell:

MVP funktionsfähig

Knowledge Base integriert

Lokale Nutzung stabil

Container-Deployment vorbereitet

CI/CD Struktur vorhanden

🔮 Geplante Erweiterungen

Azure Produktivdeployment

Authentifizierung / Access Control

Erweiterung der Knowledge Base

Azure OpenAI Integration

Observability (Monitoring / Logging)

Infrastructure as Code (Terraform/Bicep)

💡 Ziel des Projekts

Demonstration von:

Cloud Engineering Verständnis

Azure Architekturdenken

AI-gestützten Engineering-Workflows

Container-basierten Deploymentprozessen

DevOps Automatisierung

Dieses Projekt dient als Portfolio-Nachweis für eine Junior-Position im Azure / Cloud / DevOps Umfeld.
