import os

# Konu Başlıkları ve Anahtar Kelimeler
TOPICS = {
    "protection": {
        "title": "Akıllı Şebekelerde Koruma Sistemleri",
        "description": "Smart Grid Protection, Microgrid Protection, Adaptive Protection & WAMPAC",
        "arxiv_query": 'cat:eess.SY AND (abs:"smart grid protection" OR abs:"microgrid protection" OR abs:"adaptive protection")',
        "openalex_query": "smart grid protection OR microgrid protection OR adaptive protection smart grid",
        "keywords": ["smart grid protection", "microgrid protection", "adaptive protection", "wide area protection", "wampac", "relaying smart grid"]
    },
    "p2p_trading": {
        "title": "Elektrik Enerji Ticareti ve P2P",
        "description": "Peer-to-Peer Energy Trading, Transactive Energy & Local Energy Markets",
        "arxiv_query": 'cat:eess.SY AND (abs:"peer-to-peer energy" OR abs:"p2p energy" OR abs:"transactive energy")',
        "openalex_query": "peer-to-peer energy trading OR p2p energy trading OR transactive energy OR local energy market",
        "keywords": ["peer-to-peer energy", "p2p energy trading", "transactive energy", "local energy market", "blockchain energy"]
    },
    "ev_grid": {
        "title": "Elektrikli Araçların Şebekeye Etkileri",
        "description": "EV Integration, Vehicle-to-Grid (V2G), Charging Infrastructure & Grid Impacts",
        "arxiv_query": 'cat:eess.SY AND (abs:"electric vehicle" OR abs:"v2g" OR abs:"vehicle-to-grid") AND (abs:"grid" OR abs:"power system")',
        "openalex_query": "electric vehicle grid impact OR vehicle to grid OR V2G smart grid OR EV charging grid integration",
        "keywords": ["electric vehicle grid", "vehicle to grid", "v2g", "ev charging impact", "ev fleet grid"]
    }
}

# E-posta Konfigürasyonu (Ortam değişkenlerinden alınır)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Taranacak gün sayısı (Varsayılan günlük 1 gün, haftalık için 7 gün)
LOOKBACK_DAYS_DAILY = 2
LOOKBACK_DAYS_WEEKLY = 7
