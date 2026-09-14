# EduSense AI – Accelerating Educators: AI for Smarter Teaching

**Version:** 1.0
**Status:** MVP (7-Day Sprint Prototype)
**Last Updated:** October 2025

---

## 📘 Overview

**EduSense AI** is an intelligent, data-driven platform designed to empower schools and educators in Sub-Saharan Africa. It helps teachers easily generate lesson plans, teaching aids, and contextual examples aligned with the new **2025 Nigerian Curriculum Reform**.

The platform also supports personalized teacher upskilling pathways, real-time classroom support tools (AI chatbots, voice assistants, assessment generators), and works in **low-data or offline environments** — ensuring accessibility for rural and underconnected schools.

---

## 🎯 Project Objectives

1. **Generate lesson plans, teaching aids, and contextual examples** for new and existing subjects.
2. **Create personalized teacher learning pathways** to support continuous professional development.
3. **Offer real-time classroom support tools** (chatbots, voice assistants, assessment generators).
4. **Ensure accessibility and offline functionality** for schools with limited internet connectivity.

---

## 🏗️ System Architecture

### Core Modules

| Module                   | 
Description                                                           | Owner                        |
| ------------------------ | --------------------------------------------------------------------- | ---------------------------- |
| **School Management**    | Registration, teacher onboarding, access control                      | Fullstack Developer          |
| **Teacher Dashboard**    | Lesson generation, AI chat, content library, progress tracking        | Fullstack Developer          |
| **AI Engine**            | Lesson generation, contextual recommendations, upskilling suggestions | Data Scientist / AI Engineer |
| **Analytics & Insights** | Performance dashboards for teachers and admins                        | Data Analyst                 |
| **Data Infrastructure**  | Data pipelines, cloud storage, security, APIs                         | Cloud Data Engineer          |

### Architecture Overview

1. **Frontend:** ...
2. **Backend:** ...
3. **Database:** ...
4. **AI Services:** ...
5. **Analytics Layer:** ...
6. **Deployment:** ...

---

## 👩‍💻 Team Roles & Responsibilities

### 🧱 Cloud Data Engineer

* Design scalable cloud data architecture.
* Manage ETL pipelines and secure APIs for structured datasets.
* Provide clean datasets for AI and analytics modules.
* Implement authentication, storage, and logging infrastructure.

### 📊 Data Analyst

* Develop teacher and admin dashboards (progress, engagement, curriculum trends).
* Measure lesson effectiveness, completion rate, and AI tool usage.
* Ensure data quality, consistency, and version tracking.
* Work with Cloud Engineer to define schemas and update frequencies.

### 🤖 Data Scientist / AI Engineer

* Build and fine-tune models for lesson plan generation and recommendations.
* Develop teacher upskilling recommendation systems.
* Implement NLP and summarization models for chat and assessment support.
* Collaborate with frontend to expose models through REST APIs.

### 💻 Fullstack Developer

* Build responsive web dashboards for schools and teachers.
* Implement authentication (JWT, RBAC).
* Integrate APIs for lesson generation, analytics, and offline storage.
* Enable offline queue and sync with IndexedDB + background service worker.

---

## ⚙️ Key Features

### 👩🏫 School Dashboard

* Register schools and manage teacher accounts.
* Monitor teacher activity, AI usage, and curriculum progress.
* View aggregated analytics (lesson requests, engagement, upskilling status).

### 👨‍🏫 Teacher Dashboard

* Generate lesson plans and quizzes with AI.
* View personalized upskilling recommendations.
* Save and edit lesson documents (offline support).
* Sync and share materials with school library.

### 🧠 AI Support Tools

* AI chatbot and voice assistant for classroom Q&A.
* Automated assessment generator from curriculum topics.
* Difficulty analysis of curriculum topics.

### 📉 Analytics & Insights

* Progress and engagement line charts.
* Topic difficulty and learning outcome dashboards.
* Teacher effectiveness comparisons.
* Dropout and attendance monitoring.

---

## 🔒 Security & Data Governance

* JWT-based authentication and authorization.
* Encrypted data storage and communication (HTTPS, TLS).
* Audit logs for all sensitive operations.
* Compliance with local and international data protection standards.

---

## 📁 Repository Structure

- [`ai_app/`](ai_app/) — the working backend: a FastAPI service that generates curricula, MCQs, flashcards, and chat answers from class notes using Google Gemini + LangChain. See [ai_app/README.md](ai_app/README.md) for setup and API docs.
- [`frontend/`](frontend/) — the hackathon UI prototype (landing page, login, admin/student views, and dashboard pages for lesson plans, assessments, and analytics). Originally built and committed on its own unrelated branch (`warris`); merged in here so backend and frontend live in one place.

### ⚠️ Known Issues / Integration TODO

- The `frontend/` pages currently call the Gemini API **directly from the browser** with hardcoded API keys (see `ai.html`, `dashboard.html`, `dashboard/assesment.html`). Those keys are exposed in git history and must be rotated in Google AI Studio, then removed from the frontend entirely.
- Frontend and backend are not wired together yet. The plan is to point the frontend's fetch calls at the `ai_app` endpoints (`/api/v1/chat`, `/curriculum`, `/mcq`, `/flashcards`) instead of calling Gemini directly, using the `CORS_ORIGINS` setting in `ai_app` to allow the frontend's origin.

