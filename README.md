# AI for Intelligent Sales & Revenue Operations 🚀  

---

## Problem Statement 🎯

Design an AI agent that plugs into Customer Relationship Management (CRM) and communication 
systems to accelerate the sales pipeline from prospect research and personalized outreach to deal 
risk detection and revenue recovery. 

Focus areas:
- Prospect research 🔍  
- Personalized outreach ✉️  
- Deal risk detection ⚠️  
- Revenue recovery 💰  

---

## Features ⚡

- AI lead scoring with reasoning and signals  
- Automated personalized email generation  
- Deal risk detection with recovery actions  
- Churn prediction with intervention steps  
- Competitor intelligence from live news  
- Battle card generation for sales teams  
- Gmail integration for sending emails  
- Dashboard for full pipeline visibility  

---

## Tech Stack 🛠️

- Backend: FastAPI  
- Frontend: HTML, JS  
- AI: LLM powered agents  
- Integrations: Gmail, LinkedIn, News APIs  

---

## Project Structure 📁

```
revagent/
│
├── backend/
│   ├── main.py                      FastAPI app entry point
│   ├── requirements.txt
│
│   ├── agents/
│   │   ├── prospect_agent.py        Lead scoring and outreach email AI
│   │   ├── deal_agent.py            Deal risk detection and recovery AI
│   │   └── churn_agent.py           Churn prediction AI
│
│   ├── integrations/
│   │   ├── gmail_integration.py     Gmail read and send
│   │   ├── linkedin_integration.py  LinkedIn enrichment
│   │   └── news_integration.py      Competitor news tracking
│
│   ├── routes/
│   │   ├── leads.py                 Lead endpoints
│   │   ├── deals.py                 Deal endpoints
│   │   ├── churn.py                 Churn endpoint
│   │   ├── emails.py                Email endpoints
│   │   └── news.py                  Competitor signals endpoint
│
│   └── mock_data/
│       └── seed.py                  Sample dataset
│
└── frontend/
    └── index.html                  Single file dashboard
```

---

## Quick Start ⚡

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup

Open `frontend/index.html` in your browser.

- Works with mock data by default  
- Connect backend for live AI features  

---

## API Endpoints 🌐

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/dashboard              | Dashboard statistics |
| GET    | /api/leads                  | Fetch all leads |
| POST   | /api/score-lead             | Score lead and generate email |
| POST   | /api/score-all-leads        | Batch scoring |
| GET    | /api/deals                  | Fetch deals |
| POST   | /api/analyze-deal           | Deal risk analysis |
| POST   | /api/analyze-all-deals      | Batch deal analysis |
| POST   | /api/send-recovery-email    | Send recovery email |
| POST   | /api/predict-churn          | Churn prediction |
| GET    | /api/competitor-signals     | Competitor insights |

---

## Demo Flow 🎬

### 1. Lead Intake 🧲

- New lead arrives  
- Call `/api/score-lead`  

Returns:
- Score 0 to 100  
- Grade A to D  
- Reasoning  
- Key signals  

AI generates outreach email in under 2 seconds.


### 2. Outreach Execution ✉️

- Email generated with personalization  
- Sent via Gmail integration  
- Follow up email prepared  


### 3. Deal Risk Detection ⚠️

Example:
- No response for 14 days  
- Competitor mentioned  

Call `/api/analyze-deal`

Returns:
- Risk score 88  
- Level critical  
- Reasons  
- Actions  
- Recovery email  


### 4. Automated Intelligence 📊

- Competitor news detected  
- Impacted deals identified  

Example:
- 2 deals  
- Value 320K  

Battle card:
> 2 weeks vs 6 months implementation  


### 5. Recovery Execution 🔁

- Call `/api/send-recovery-email`  
- Email sent via Gmail  
- Deal re engaged  

---


### Revenue Impact 💰

```
Additional deals:
6% increase x 50 x $85,000 = $255,000 per month

Faster cycle:
18 days improvement = $140,000 unlocked

Churn recovery:
3% x $48,000 x 5 = $7,200

Total:
~$402,200 per month
~$4.8M annually

Savings:
24 hours x $80 = $1,920 per month
~₹1,60,000 per month

6 month estimate:
~₹83,00,000
```

---

## AI Architecture 🧠

```
Lead Signal
    ↓
ProspectAgent
    → score, grade, email
    ↓
Gmail


Deal Data
    ↓
DealAgent
    → risk, actions, email
    ↓
Alert system


Usage Data
    ↓
ChurnAgent
    → probability, actions
    ↓
CS team


News API
    ↓
Competitor signals
    ↓
Sales alerts
```

---

## Environment Variables 🔐

```
NEWS_API_KEY=your_newsapi_key
ANTHROPIC_API_KEY=your_key
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
```

---

## Contributors 👨‍💻

- Mayur Bhong 
- Kartik Sawant  
- Aditya Pol
- Prathamesh Kharade 

---

## Future Improvements 🔮

- CRM integrations like Salesforce and HubSpot  
- Real time Slack and WhatsApp alerts  
- Advanced analytics dashboard  
- Multi language outreach support  
