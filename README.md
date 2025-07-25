# 🩺 ArogyaBot (MedicalGPT)

TEAM(SC)2-10 
# 🩺 AarogyaBot – AI Medical Assistant

📎 [Download TEAM(SC)2-10 Report (PDF)](https://github.com/next-pratik/arogyaBot/blob/main/TEAM(SC)2-10.pdf)  
*(Right-click the link and choose “Save link as…” to download)*

# YOU MAY VISIT :- https://arogyabot.streamlit.app/
(It may be slow have some patient)
(The model is trained on docs not a complete data set. Tavily is used but in some cases it may not be effective there may be exception happen since this is not the best trained bot but we tried our level best)
For any query write to the developer 23cse579.pratikkumarsah@giet.edu,

![Team](https://img.shields.io/badge/Team-Team(SC)2--10-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![LLM](https://img.shields.io/badge/LLM-Gemini-purple.svg)

> **Empowering India's rural communities with AI-driven healthcare—accessible, multilingual, and real-time.**

---

##  Team Details

| Role         | Name              |
|--------------|-------------------|
| Team Name    | Team (SC)2–10     |
| Member (LEAD)| Sidhu Kumar Singh |
| Member       | Pratik Kumar Sah  |
| Member       | Ankit Biswal      |

---

## Project Overview

**AarogyaBot** is a multilingual AI-powered health assistant tailored for India’s underserved regions. It bridges the healthcare gap by offering preliminary medical advice in local languages, powered by real-time web search, LLMs, and government-backed translation tools.

---

## Tech Stack

| Category       | Technology       | Purpose                                 |
|----------------|------------------|-----------------------------------------|
| Backend        | Python           | Core logic and LLM orchestration        |
| LLM            | Google Gemini    | Natural language understanding & output |
| AI Framework   | LangChain        | Tool routing and context handling       |
| Web Search     | Tavily API       | Live, real-time health info             |
| Translation    | Google Translate | Multilingual support (text + speech)    |
| Frontend       | Streamlit        | User interface                          |
| Vector Store   | FAISS            | Retrieval-Augmented Generation (RAG)    |
| Testing        | Pytest           | Test RAG & search modules               |

---

##  Key Features

-  **Symptom Checker (RAG + Gemini):** Ask about your symptoms and get a possible condition summary.
-  **Live Web Search (Tavily):** Ensures health advice is based on current data.
-  **Multilingual Interaction (Bhashini):** Understands and responds in local Indian languages.
-  **Preliminary Report Generation:** Summarizes potential diagnoses and next steps.
-  **Minimal UI:** Fast, lightweight, and designed for low-bandwidth use.

---

##  How to Run the Project Locally

### A. Setup Environment

```bash
git clone https://github.com/next-pratik/arogyaBot.git
cd arogyaBot

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### B. Install Requirements

```bash
pip install -r requirements.txt
```

### C. Configure API Keys

Create a `.env` file with the following:

```env
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
```

(*Add Bhashini credentials as needed*)

### D. Launch the App

```bash
streamlit run streamlit_app.py
```

---

## Problem Statement

In rural India, delays in diagnosis due to doctor unavailability, language gaps, and low digital literacy cause poor health outcomes. **AarogyaBot** offers an always-available, multilingual AI to empower self-diagnosis and bridge the accessibility gap.

---

## Stakeholders & Impact

| Stakeholder        | Value Provided                                     |
|--------------------|----------------------------------------------------|
| Rural Patients     | 24/7 multilingual medical advice                   |
| ASHA/Health Workers| Instant pre-screening and reduced burden          |
| Doctors/Hospitals  | Structured pre-diagnostic reports                  |
| Public Health Orgs | Anonymized regional health trend data              |

---

## Success Metrics (KPIs)

| Metric            | Target      | Notes                                       |
|-------------------|-------------|---------------------------------------------|
| AI Accuracy       | ≥ 85%       | Relevance of symptom mapping                |
| Language Support  | ≥ 5         | Via Bhashini API                            |
| Daily Users       | 1K+         | Especially from rural zones                 |
| System Uptime     | ≥ 99.5%     | For always-on accessibility                 |

---

## Future Scope

- **Full Voice Support** (STT + TTS)
- **Offline Mode** for zero-connectivity regions
- **EHR Integration** for care continuity
- **Predictive Analytics** on regional health trends

---

## Note on API Keys

You **must** configure your own keys for:

- `Google Gemini` -->
- `Tavily` -->
- *(Bhashini credentials via NIC portal)*

---

## Final Words

> AarogyaBot isn't just a chatbot—it's a **lifesaving frontline health assistant** tailored for India's most vulnerable. With real-time AI and language inclusivity, we’re making healthcare more human, more reachable, and more **democratic**.
