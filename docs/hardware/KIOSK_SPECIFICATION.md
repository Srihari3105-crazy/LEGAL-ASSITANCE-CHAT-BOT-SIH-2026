# SahkarSetu Rural Kiosk — Hardware Specification

## Overview

The SahkarSetu Rural Kiosk is a low-cost, self-contained computing device designed to be deployed at PACS offices, Gram Panchayat buildings, cooperative bank branches, and CSC centers across India. It runs the full SahkarSetu platform in kiosk mode, providing voice-enabled cooperative governance assistance to rural members who may not own smartphones or have internet access.

---

## Hardware Bill of Materials

| Component | Specification | Purpose | Estimated Cost (₹) |
|-----------|--------------|---------|---------------------|
| Raspberry Pi 5 (8GB RAM) | Quad-core ARM Cortex-A76, 2.4GHz | Main compute unit | ₹6,500 |
| 10.1" IPS Touchscreen | 1280×800, capacitive touch, HDMI | User interface display | ₹4,000 |
| USB Microphone | Omnidirectional, noise-cancelling | Voice input (STT) | ₹800 |
| USB/Bluetooth Speaker | 3W, clear voice output | Voice output (TTS) | ₹500 |
| 4G LTE USB Dongle | SIM-based internet connectivity | Network connection | ₹1,500 |
| microSD Card (128GB) | Class 10, A2 rated | OS + application storage | ₹800 |
| Weatherproof Enclosure | Powder-coated metal + acrylic front | Physical protection | ₹2,000 |
| UPS / Battery Backup | 12V 7Ah, 4-hour runtime | Power backup for outages | ₹2,000 |
| Solar Panel (optional) | 20W monocrystalline, charge controller | Remote area power | ₹3,000 |
| Cables & Mounting | HDMI, USB, power supply, wall mount | Assembly | ₹500 |
| **TOTAL (without solar)** | | | **₹18,600** |
| **TOTAL (with solar)** | | | **₹21,600** |

---

## Software Configuration

### Operating System
- **Raspberry Pi OS Lite (64-bit)** — minimal overhead
- **Chromium in Kiosk Mode** — full-screen SahkarSetu web interface
- **Auto-start on boot** — no login required

### Kiosk Mode Setup
```bash
# Auto-login to CLI
sudo raspi-config → Boot Options → Console Autologin

# Install Chromium
sudo apt install -y chromium-browser

# Create kiosk launcher script
cat > /home/pi/kiosk.sh << 'EOF'
#!/bin/bash
xset s off
xset -dpms
xset s noblank
chromium-browser \
  --noerrdialogs \
  --disable-infobars \
  --kiosk \
  --incognito \
  --disable-translate \
  --no-first-run \
  --fast \
  --fast-start \
  --disable-features=TranslateUI \
  http://localhost:5173
EOF
chmod +x /home/pi/kiosk.sh

# Autostart on boot
echo "@/home/pi/kiosk.sh" >> /etc/xdg/lxsession/LXDE-pi/autostart
```

### Offline Mode
- **Ollama** runs locally on Pi 5 (Qwen 2.5 7B quantized to Q4_0)
- **FAISS index** pre-loaded with cooperative law documents
- **Whisper** (base model) for offline speech recognition
- **pyttsx3** for offline text-to-speech
- Periodic sync when 4G connection is available

---

## Network Architecture

```
           ┌─────────────────┐
           │  CENTRAL SERVER  │
           │  (Cloud/VPS)     │
           │  - Full LLM API  │
           │  - Data sync     │
           │  - Analytics     │
           └────────┬────────┘
                    │ 4G/WiFi
        ┌───────────┼───────────┐
        ▼           ▼           ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ KIOSK 1  │ │ KIOSK 2  │ │ KIOSK N  │
  │ PACS     │ │ Gram     │ │ Coop     │
  │ Office   │ │ Panchayat│ │ Bank     │
  │ (Pi 5)   │ │ (Pi 5)   │ │ (Pi 5)   │
  └──────────┘ └──────────┘ └──────────┘
```

- **Online Mode**: Queries routed to central server (Groq LLM + Sarvam AI voice)
- **Offline Mode**: Falls back to local Ollama LLM + Whisper STT + pyttsx3 TTS
- **Sync**: Grievances, usage analytics, and knowledge base updates synced when online

---

## Deployment Plan

### Phase 1: Pilot (50 kiosks)
- Deploy in 50 PACS offices across 5 states (10 per state)
- States: Maharashtra, Uttar Pradesh, Rajasthan, Tamil Nadu, West Bengal
- Total cost: 50 × ₹18,600 = **₹9.3 lakh**

### Phase 2: Scale (5,000 kiosks)
- Deploy in District Central Cooperative Bank branches + PACS offices
- Leverage PACS Computerization infrastructure
- Total cost: 5,000 × ₹18,600 = **₹9.3 crore**

### Phase 3: National Scale (63,000+ PACS)
- One kiosk per computerized PACS office
- Integrated with National Cooperative Database
- Total cost: 63,000 × ₹18,600 = **₹117 crore** (negligible compared to PACS computerization budget of ₹2,516 crore)

---

## Accessibility Features

1. **Voice-First Interface** — Large microphone button, speak in any of 12 Indian languages
2. **Large Touch Targets** — Minimum 48px touch areas for elderly users
3. **High Contrast Display** — Dark mode optimized for bright outdoor conditions
4. **Audio Feedback** — Every action confirmed with voice in user's language
5. **No Typing Required** — Full interaction possible through voice alone
6. **Multilingual UI** — Hindi + English toggle, voice in 12 languages
7. **Session Timeout** — Auto-reset after 5 minutes of inactivity (privacy)

---

## Maintenance

- **Remote Management**: SSH access for software updates
- **OTA Updates**: Knowledge base updates pushed via 4G connection
- **Self-Healing**: Watchdog timer auto-restarts crashed services
- **Monitoring**: Heartbeat pings to central server for uptime tracking
- **Local Backup**: SQLite database backed up daily to microSD
