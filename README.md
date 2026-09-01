# SahkarSetu (सहकार सेतु) — Cooperative Governance & Legal Assistance Chatbot

### 🏆 SIH 2026 | Problem Statement ID: 26088 | Ministry of Cooperation (NCCT)

> **Speak Your Language. Know Your Cooperative Rights. Get Heard.**

AI-powered multilingual chatbot providing instant guidance on cooperative governance, legal provisions, schemes, and member services. Built for cooperative members, farmers, and rural stakeholders across India.

---

## 🎯 Problem Statement

Cooperative members, farmers, and rural stakeholders lack awareness regarding:
- Cooperative laws and by-laws
- Government schemes and PACS services
- Crop insurance (PMFBY) procedures
- Financial literacy for cooperative banking
- Grievance redressal mechanisms

**Root Cause**: Language barriers + limited digital access + no voice pathway for illiterate users.

**Our Solution**: An offline-capable, voice-native, multilingual AI platform that works even without internet.

---

## ✨ Key Features

| Feature | Description | Languages |
|---------|-------------|-----------|
| 🗣️ **SahkarVaani Voice Engine** | Speak your query in any Indian language — get voice response | 12 languages |
| ⚖️ **Cooperative Law Advisor** | Guidance on MSCS Act 2002, State Acts, Model Bye-Laws | Hindi + English |
| 🌾 **PMFBY Assistant** | Crop insurance eligibility, premium calculator, claim guidance | Multilingual |
| 🏦 **PACS Services Guide** | Membership, loans, KCC, multipurpose PACS activities | Multilingual |
| 💰 **Financial Literacy** | Cooperative banking, savings, loan management, SHG guide | Multilingual |
| 📋 **Cooperative Grievance Portal** | File, track, and escalate cooperative complaints with SLA | All supported |
| 📢 **Notice Drafter** | AI-generated cooperative circulars and official notices | Hindi + English |
| 🔒 **Offline-First** | Full functionality without internet via local LLM | All features |
| 🖥️ **Rural Kiosk Ready** | ₹18,600 Raspberry Pi kiosk for PACS offices | Hardware spec |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (Desktop/Web/Kiosk)              │
│           React 18 + TypeScript + Vite 5 + Tailwind          │
│    Role-adaptive UI (Member/Officer/Admin) | 12+ pages       │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP (Bearer JWT)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              FASTAPI GATEWAY (port 8001)                      │
│    CORS | Rate Limiting | Security Headers | Request Logging  │
│                                                               │
│  ┌─────────┐ ┌────────┐ ┌──────────┐ ┌────────┐ ┌────────┐  │
│  │  Auth   │ │Schemes │ │Grievance │ │ Notice │ │ Admin  │  │
│  │12 endpt │ │15+ endp│ │30+ endpt │ │13 endpt│ │14 endpt│  │
│  └────┬────┘ └───┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘  │
│       └──────────┼───────────┼────────────┼──────────┘       │
│                  ▼           ▼            ▼                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                   RAG ENGINE                          │    │
│  │  Chunker → Embedder (768d) → FAISS → LLM (Groq/     │    │
│  │  Ollama) → Anti-Hallucination (6 layers) → Citations │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌──────────────────────▼───────────────────────────────┐    │
│  │             SAHKARVAANI VOICE ENGINE                   │    │
│  │  ASR (Sarvam/Whisper) → Intent → TTS (Bulbul/pyttsx3)│    │
│  │  Translation (Mayura/Ollama) - 12 Indian languages    │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────┬───────────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
     ┌──────────┐ ┌─────────┐ ┌──────────┐
     │ SQLite   │ │  FAISS  │ │  Ollama  │
     │ 20+ tbl  │ │  768d   │ │ Qwen 14B │
     │ WAL mode │ │  index  │ │ localhost│
     └──────────┘ └─────────┘ └──────────┘
```

---

## 📚 Knowledge Base

| Domain | Documents | Coverage |
|--------|-----------|----------|
| Cooperative Laws | MSCS Act 2002, Amendment 2023, Model Bye-Laws | Registration, membership, governance, audit, disputes |
| PACS Services | PACS Guide, Computerization Project, Multipurpose PACS | 25+ activities, membership, loan process |
| PMFBY | Crop Insurance Guide, Premium Tables, Claim Procedures | Eligibility, premium calc, claim filing, risk coverage |
| Financial Literacy | Cooperative Banking, KCC, Savings, SHGs | Loan management, savings options, credit education |
| Grievance Redressal | Member Rights, Filing Process, Election Disputes | Multi-channel redressal, escalation paths |
| Ministry of Cooperation | Sahkar-se-Samriddhi, AIF, NCDC, NCCT Programs | All major cooperative schemes |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) (for offline LLM)
- 16GB RAM recommended

### Backend
```bash
# Pull the LLM model (~5GB one-time download)
ollama pull qwen2.5:14b-instruct-q4_0

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys (Groq, Sarvam AI)

# Start the API server
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd desktop
npm install
npm run dev
```

### Docker (One-Command Deploy)
```bash
docker-compose up -d
```

---

## 🔑 API Keys (Free Tiers Available)

| Service | Purpose | Free Tier | Get Key |
|---------|---------|-----------|---------|
| **Groq** | LLM inference (Llama 3.3 70B) | Free tier | [console.groq.com](https://console.groq.com) |
| **Sarvam AI** | Voice STT/TTS (22 Indian languages) | ₹1000 credits | [dashboard.sarvam.ai](https://dashboard.sarvam.ai) |
| **Ollama** | Offline LLM (runs locally) | 100% free | [ollama.com](https://ollama.com) |

---

## 🌍 Supported Languages

### Voice (STT + TTS): 12 Languages
Hindi, English, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese

### UI: Bilingual
English + Hindi (extensible to more via i18n)

---

## 🏛️ Cooperative Grievance Categories

| Category | Department | SLA |
|----------|-----------|-----|
| Membership Denial | Cooperative Governance | 14 days |
| Dividend Dispute | Membership Issues | 30 days |
| Election Irregularity | Cooperative Governance | 7 days |
| Loan Recovery Harassment | Credit Disputes | 14 days |
| Insurance Claim Delay | Insurance Claims | 30 days |
| PACS Service Denial | PACS Services | 14 days |
| Corruption | Cooperative Governance | 45 days |
| By-Law Violation | Audit & Compliance | 30 days |

---

## 🖥️ Hardware Kiosk (₹18,600)

Designed for deployment at PACS offices and Gram Panchayats:
- **Raspberry Pi 5** (8GB) + 10.1" touchscreen
- **Voice-first**: USB mic + speakers for illiterate users
- **Offline-capable**: Local LLM + Whisper + pyttsx3
- **Solar-powered variant** for remote areas (+₹3,000)
- **Scales to 63,000+ PACS** offices nationwide

See [Kiosk Specification](docs/hardware/KIOSK_SPECIFICATION.md) for full details.

---

## 🛡️ Security & Privacy

- **6-layer anti-hallucination** system prevents false legal advice
- **JWT authentication** with role-based access control
- **Data sovereignty**: Offline mode keeps all data on-device
- **Input sanitization**: Protection against prompt injection
- **Rate limiting**: 100 requests/minute per IP
- **DPDP compliance**: No personal data stored without consent

---

## 📁 Project Structure

```
SahkarSetu/
├── src/
│   ├── api/                    # FastAPI routes & middleware
│   │   ├── app.py              # Main application
│   │   ├── grievance_routes.py # Cooperative grievance endpoints
│   │   ├── scheme_routes.py    # Scheme information endpoints
│   │   └── ...
│   ├── core/                   # RAG engine (chunker, embedder, retriever)
│   ├── generation/             # LLM client, prompt templates
│   └── modules/
│       ├── sahkarvaani/        # Voice engine (ASR, TTS, translation)
│       ├── grievance_router.py # AI-powered grievance classification
│       ├── summarizer.py       # Scheme summarization
│       └── notice_drafter.py   # Cooperative notice generation
├── data/
│   ├── formatted_docs/         # Cooperative knowledge base (JSON)
│   └── schemes_seed.json       # Cooperative scheme catalog
├── desktop/                    # React frontend (Vite + TypeScript)
├── docs/
│   └── hardware/               # Kiosk specification
├── docker-compose.yml          # One-command deployment
├── Dockerfile                  # Container image
└── requirements.txt            # Python dependencies
```

---

## 🏆 Why This Wins

| Differentiator | Impact |
|---------------|--------|
| **Offline-first** | Works in villages with no internet |
| **Hardware kiosk (₹18.6K)** | Addresses "Hardware" category — most teams miss this |
| **6-layer anti-hallucination** | Safe legal advice — no false cooperative law citations |
| **Voice in 12 languages** | Accessible to illiterate rural members |
| **Cooperative-specific RAG** | MSCS Act, PACS, PMFBY — not generic government info |
| **SLA-tracked grievances** | Government accountability mechanism |
| **Government tech alignment** | Uses Sarvam AI / Bhashini (India-made) |
| **Citation-backed responses** | Every answer references exact law sections |
| **Role-based access** | Member, Officer, Admin — complete ecosystem |
| **₹18.6K kiosk → 63K PACS** | Scalable national deployment plan |

---

## 📜 License

Apache-2.0 License — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Ministry of Cooperation** & NCCT for the problem statement
- **Sarvam AI** for Indian language voice technology
- **Groq** for fast LLM inference
- **FAISS** (Meta) for vector similarity search
- Built with ❤️ for India's cooperative movement — **Sahkar se Samriddhi** 🇮🇳
