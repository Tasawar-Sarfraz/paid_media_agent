# 📈 Paid Media AI Agent Dashboard

An enterprise-grade, real-time marketing analytics dashboard built with **Streamlit**, **LangChain**, and **Groq (openai/gpt-oss-120b)**. 
The application ingests paid campaign data across multi-channel networks (Google Ads & Meta Ads) and computes deterministic KPIs alongside 
LLM-powered strategic insights.

---

## 🌟 Key Features

- **Multi-Source Data Ingestion:**
  - **Manual Input:** Interactive sidebar controls for real-time scenario simulation.
  - **CSV Upload:** Auto-parsing with column normalization and state persistence.
  - **Google Sheets Sync:** Direct integration with public Google Sheets export URLs.
- **Deterministic Math Engine:**
  - Calculates Total Spend, Overall CPC, MQLs, Pipeline, Actual CPA, and Target CPA Variance with zero LLM math hallucination.
- **Real-Time Reactive Dashboard:**
  - Custom UI metric cards with dynamic color coding based on CPA targets.
  - Embedded Matplotlib visualizations for spend distribution and target performance.
- **LangChain & Groq Orchestration:**
  - Powered by `openai/gpt-oss-120b` to deliver structured, Slack-ready marketing strategic briefs.

---

## 🛠️ Tech Stack

- **Frontend / App Framework:** [Streamlit](https://streamlit.io/)
- **Data Handling:** Pandas, Matplotlib
- **LLM Orchestration:** LangChain Core, LangChain Groq
- **Inference Engine:** Groq API (`openai/gpt-oss-120b`)
- **Language:** Python 3.10+

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/paid-media-ai-agent.git](https://github.com/your-username/paid-media-ai-agent.git)
   cd paid-media-ai-agent
