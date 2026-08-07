import os

# Konu Başlıkları ve Anahtar Kelimeler (Nokta Atışı Teknik Terimler)
TOPICS = {
    "protection": {
        "title": "Akıllı Şebekelerde Koruma Sistemleri",
        "description": "Smart Grid Protection, Microgrid Protection, Adaptive Relaying & WAMPAC",
        "arxiv_query": 'cat:eess.SY AND ("smart grid protection" OR "microgrid protection" OR "adaptive protection")',
        "openalex_query": '"smart grid protection" OR "microgrid protection" OR "adaptive protection smart grid"',
        "keywords": ["smart grid protection", "microgrid protection", "adaptive protection", "wide area protection", "wampac"]
    },
    "p2p_trading": {
        "title": "Elektrik Enerji Ticareti ve P2P",
        "description": "Peer-to-Peer Energy Trading, Transactive Energy & Local Energy Markets",
        "arxiv_query": 'cat:eess.SY AND ("peer-to-peer energy trading" OR "p2p energy trading" OR "transactive energy")',
        "openalex_query": '"peer-to-peer energy trading" OR "p2p energy trading" OR "transactive energy market"',
        "keywords": ["peer-to-peer energy trading", "p2p energy trading", "transactive energy", "local energy market"]
    },
    "ev_grid": {
        "title": "Elektrikli Araçların Şebekeye Etkileri",
        "description": "EV Grid Integration, Vehicle-to-Grid (V2G) & Charging Impacts",
        "arxiv_query": 'cat:eess.SY AND ("vehicle-to-grid" OR "v2g" OR "electric vehicle grid integration")',
        "openalex_query": '"vehicle to grid" OR "v2g smart grid" OR "electric vehicle grid integration"',
        "keywords": ["electric vehicle grid impact", "vehicle to grid", "v2g", "ev grid integration"]
    }
}

# E-posta Konfigürasyonu (Ortam değişkenlerinden alınır)
SMTP_SERVER = os.getenv("SMTP_SERVER") or "smtp.gmail.com"
raw_port = os.getenv("SMTP_PORT", "").strip()
SMTP_PORT = int(raw_port) if raw_port.isdigit() else 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Taranacak gün sayısı (Varsayılan günlük 2 gün, haftalık için 7 gün)
LOOKBACK_DAYS_DAILY = 2
LOOKBACK_DAYS_WEEKLY = 7
