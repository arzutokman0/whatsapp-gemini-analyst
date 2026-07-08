#  AI-Powered WhatsApp Document & Image Analyst Bot

[TR] Bu proje, WhatsApp üzerinden gönderilen görsel ve PDF belgelerini anlık olarak analiz eden, yapay zeka destekli üretime hazır bir FastAPI arka uç (backend) servisidir.
[EN] This project is a production-ready FastAPI backend service that instantly analyzes images and PDF documents sent via WhatsApp using advanced AI.

---

##  English Description & Setup

###  Project Overview
This repository contains a FastAPI backend integrated with Twilio's WhatsApp Business API and Google's Gemini 2.5-Flash model. The system functions as an intelligent AI Agent capable of receiving documents and images directly from a WhatsApp chat, processing raw binary streams, and responding with precise, concise summaries.

Key challenges overcome during development:
* **Dynamic MIME-Type Extraction:** Fixed standard multi-media streaming bugs by analyzing raw byte signatures (`%PDF` headers) to correctly flag incoming data packets.
* **Bypassing Security Blockades:** Resolved HTTP `401 Unauthorized` and `400 Invalid Argument` errors caused by Twilio Sandbox's rigid media authentication constraints.
* **Stable Local Development:** Replaced unstable ephemeral tunnels with secure static ngrok routing to maintain consistent webhook connectivity.

###  Tech Stack
* **Backend Framework:** FastAPI (Python 3.10+)
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Communication API:** Twilio WhatsApp Business Sandbox
* **Tunneling:** ngrok (Static Domain)

###  Quick Start
1. **Clone the repository:**
```bash
   git clone <your-repository-url>
   cd whatsapp-rag-assistant

2. Setup Environment Variables: Create a .env file in the root directory:

Kod snippet'i
GEMINI_API_KEY=your_gemini_api_key_here
Run the server:

Bash
uvicorn main:app --reload
Start the Tunnel:

Bash
ngrok http --url=slacked-banshee-pushup.ngrok-free.dev 8000
Configure your Twilio WhatsApp Sandbox webhook URL to: https://slacked-banshee-pushup.ngrok-free.dev/webhook
   ```bash
   git clone <your-repository-url>
   cd whatsapp-rag-assistant
