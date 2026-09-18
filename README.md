# 📈 Paid Media AI Agent Dashboard

> **Enterprise-grade, real-time marketing analytics powered by Streamlit, LangChain, and Groq.**

A powerful AI-driven **Paid Media Analytics Dashboard** that ingests multi-channel campaign data from **Google Ads and Meta Ads**, calculates deterministic marketing KPIs, and generates **LLM-powered strategic insights** for marketing teams.

The application combines a reliable mathematical KPI engine with AI-generated recommendations — ensuring that **critical marketing calculations remain deterministic while AI focuses on analysis and strategy.**

---

## ✨ Features

### 📊 Multi-Source Data Ingestion

The dashboard supports multiple ways to provide campaign data:

* 📝 **Manual Input**

  * Interactive sidebar controls
  * Real-time scenario simulation
  * Quickly test different campaign scenarios

* 📁 **CSV Upload**

  * Automatic CSV parsing
  * Column normalization
  * Persistent application state

* 📗 **Google Sheets Sync**

  * Connect directly to public Google Sheets
  * Automatic data ingestion through export URLs
  * Useful for continuously updated campaign data

---

### 🧮 Deterministic KPI Engine

All critical marketing calculations are handled by a deterministic math engine instead of relying on the LLM.

The dashboard calculates:

| KPI                        | Description                                |
| -------------------------- | ------------------------------------------ |
| 💰 **Total Spend**         | Combined advertising spend across channels |
| 🖱️ **Overall CPC**        | Cost per click across campaigns            |
| 🎯 **MQLs**                | Total Marketing Qualified Leads            |
| 💼 **Pipeline**            | Total generated pipeline value             |
| 💵 **Actual CPA**          | Actual cost per acquisition                |
| 📈 **Target CPA Variance** | Difference between actual and target CPA   |

> **Why deterministic calculations?**
> Marketing KPIs should not depend on LLM reasoning. The application calculates the numbers programmatically and uses the LLM primarily for interpretation and strategic recommendations.

---

### ⚡ Real-Time Reactive Dashboard

The dashboard dynamically updates whenever campaign inputs change.

Features include:

* 🎨 Custom metric cards
* 🔴🟢 Dynamic KPI color coding
* 🎯 Target CPA performance indicators
* 📊 Spend distribution visualizations
* 📈 Target performance charts
* 🔄 Real-time scenario updates

---

### 🤖 AI-Powered Marketing Insights

The application uses **LangChain + Groq** to transform campaign performance data into actionable marketing insights.

Powered by:

> **`openai/gpt-oss-120b`**

The AI generates structured, **Slack-ready strategic briefs** covering campaign performance, opportunities, risks, and recommended actions.

---

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │   Campaign Sources   │
                  └──────────┬───────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
       Manual Input       CSV Upload    Google Sheets
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                  ┌──────────────────────┐
                  │   Pandas Data Layer  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Deterministic KPI    │
                  │      Engine          │
                  └──────────┬───────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
             KPI Dashboard      Campaign Data
                    │                 │
                    └────────┬────────┘
                             ▼
                  ┌──────────────────────┐
                  │ LangChain + Groq    │
                  │   AI Orchestration   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Strategic Marketing  │
                  │       Brief          │
                  └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                            |
| --------------------- | ---------------------------------- |
| 🖥️ **Streamlit**     | Frontend and application framework |
| 🐼 **Pandas**         | Data processing and transformation |
| 📊 **Matplotlib**     | Data visualization                 |
| 🔗 **LangChain Core** | LLM orchestration                  |
| ⚡ **LangChain Groq**  | Groq model integration             |
| 🧠 **Groq API**       | High-speed LLM inference           |
| 🤖 **GPT-OSS 120B**   | AI-powered marketing analysis      |
| 🐍 **Python 3.10+**   | Application development            |

---

## 📋 Data Schema

Your CSV file or Google Sheet should contain the following columns:

| Column          | Description                     | Example      |
| --------------- | ------------------------------- | ------------ |
| `date`          | Campaign date                   | `2026-09-01` |
| `google_spend`  | Google Ads spend ($)            | `2500`       |
| `google_clicks` | Google Ads clicks               | `1250`       |
| `meta_spend`    | Meta Ads spend ($)              | `1800`       |
| `meta_clicks`   | Meta Ads clicks                 | `1100`       |
| `mqls`          | Marketing Qualified Leads       | `85`         |
| `pipeline`      | Pipeline value ($)              | `25000`      |
| `target_cpa`    | Target Cost Per Acquisition ($) | `50`         |

### Example CSV

```csv
date,google_spend,google_clicks,meta_spend,meta_clicks,mqls,pipeline,target_cpa
2026-09-01,2500,1250,1800,1100,85,25000,50
2026-09-02,2800,1400,1950,1200,92,28000,50
2026-09-03,2200,1100,1750,1050,78,23000,50
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/paid-media-ai-agent.git
```

Navigate into the project:

```bash
cd paid-media-ai-agent
```

---

### 2️⃣ Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Or configure the environment variable directly.

### Linux / macOS

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

> 🔐 **Security:** Never commit your `.env` file or API keys to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

---

### 4️⃣ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

## 📊 Dashboard Workflow

The application follows a simple workflow:

### Step 1 — Provide Campaign Data

Choose one of the supported data sources:

```text
Manual Input
     │
     ├── Google Ads
     └── Meta Ads

OR

CSV Upload

OR

Google Sheets
```

### Step 2 — Calculate KPIs

The deterministic engine processes the campaign data and calculates:

```text
Total Spend
     ↓
Total Clicks
     ↓
Overall CPC
     ↓
MQLs
     ↓
Actual CPA
     ↓
Target CPA Variance
```

### Step 3 — Visualize Performance

The dashboard displays:

* Spend distribution
* Campaign performance
* Target CPA comparison
* Marketing KPIs

### Step 4 — Generate AI Insights

The calculated metrics are provided to the LLM for strategic interpretation.

The AI produces a structured marketing brief that can be shared with stakeholders or marketing teams.

---

## 🤖 AI Strategic Brief

The AI layer is designed to focus on **interpretation rather than mathematical calculation**.

For example:

```text
Campaign Data
      ↓
Deterministic KPI Engine
      ↓
Verified Metrics
      ↓
LLM Analysis
      ↓
Strategic Insights
      ↓
Slack-Ready Brief
```

This architecture helps reduce the risk of **LLM-generated mathematical errors** while still benefiting from generative AI for strategic analysis.

---

## 🎯 Key Design Principles

### 1. Deterministic First

Critical business metrics are calculated using code rather than asking the LLM to perform the calculations.

### 2. AI for Interpretation

The LLM is used to identify patterns, opportunities, risks, and potential marketing actions.

### 3. Real-Time Feedback

Changing campaign inputs immediately updates the dashboard and calculated KPIs.

### 4. Multi-Channel Analysis

Google Ads and Meta Ads data can be analyzed together to provide a unified view of paid media performance.

### 5. Business-Ready Output

AI-generated insights are structured into concise briefs suitable for sharing with marketing teams and stakeholders.

---

## 📁 Suggested Project Structure

```text
paid-media-ai-agent/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── data/
│   └── campaign_data.csv
│
└── assets/
    └── screenshots/
```

---

## 📦 Requirements

The project requires:

```text
Python 3.10+
Streamlit
Pandas
Matplotlib
LangChain Core
LangChain Groq
Groq API
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Required environment variable:

| Variable       | Required | Description                         |
| -------------- | -------- | ----------------------------------- |
| `GROQ_API_KEY` | ✅ Yes    | API key used for Groq LLM inference |

Example:

```env
GROQ_API_KEY=your_api_key
```

---

## 📈 Example Use Case

A marketing team wants to understand how its paid advertising campaigns are performing.

Instead of manually calculating KPIs and analyzing campaign data:

```text
Google Ads Data ─┐
                 │
                 ├──► Paid Media AI Agent
                 │
Meta Ads Data ───┘
                         │
                         ▼
                  KPI Calculations
                         │
                         ▼
                  Performance Charts
                         │
                         ▼
                   AI Analysis
                         │
                         ▼
              Strategic Marketing Brief
```

The team can therefore move from **raw campaign data → verified metrics → strategic insights** within a single dashboard.

---

## 🚧 Future Improvements

Potential future enhancements include:

* 🔄 Live Google Ads API integration
* 🔄 Live Meta Marketing API integration
* 📅 Historical campaign trend analysis
* 📊 Additional marketing attribution metrics
* 🚨 Automated campaign anomaly detection
* 🔔 Slack notifications
* 📧 Email reports
* ☁️ Cloud deployment
* 👥 Role-based access control
* 📈 Advanced forecasting

---

## 🌐 Deployment

The application can be deployed using Streamlit-compatible hosting or other cloud platforms.

Before deployment, make sure the following environment variable is configured securely:

```text
GROQ_API_KEY
```

Do **not** expose API keys inside source code.

---

## 📄 License

Add your preferred license here, for example:

```text
MIT License
```

---

## 👨‍💻 Author

**TASAWAR SARFRAZ**

Built with:

**Python • Streamlit • Pandas • Matplotlib • LangChain • Groq • Generative AI**

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Paid Media AI Agent — turning campaign data into actionable marketing intelligence.** 🚀
