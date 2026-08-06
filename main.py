import sys
import os
import argparse
import logging
from datetime import datetime
from config import TOPICS, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, GEMINI_API_KEY
from fetchers import PaperFetcher
from summarizer import PaperSummarizer
from mailer import Mailer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline(mode: str = "daily"):
    logging.info(f"Yayın Tarama Otomasyonu Başlatıldı. Mod: {mode}")
    
    days_back = 7 if mode == "weekly" else 2
    fetcher = PaperFetcher(days_back=days_back)
    summarizer = PaperSummarizer(api_key=GEMINI_API_KEY)
    
    topic_results = {}
    total_papers_found = 0

    for topic_key, topic_config in TOPICS.items():
        logging.info(f"Makaleler taranıyor: {topic_config['title']}...")
        raw_papers = fetcher.fetch_for_topic(topic_config)
        logging.info(f"Bulunan makale sayısı: {len(raw_papers)}")
        
        # Günlük modda makaleleri Türkçe özetle
        summarized_papers = summarizer.summarize_daily_papers(topic_config["title"], raw_papers)
        
        topic_results[topic_key] = {
            "config": topic_config,
            "papers": summarized_papers
        }
        total_papers_found += len(summarized_papers)

    # Rapor Kaydetme (Klasöre yedek alma)
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join(os.path.dirname(__file__), "reports", today_str)
    os.makedirs(output_dir, exist_ok=True)

    mailer = Mailer(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)
    recipient = RECIPIENT_EMAIL or SENDER_EMAIL

    if mode == "daily":
        html_content = mailer.build_daily_html(topic_results)
        file_path = os.path.join(output_dir, f"daily_report_{today_str}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(f"Günlük rapor dosyası oluşturuldu: {file_path}")

        subject = f"⚡ Günlük Güç Sistemleri Makale Raporu ({today_str}) - {total_papers_found} Yeni Yayın"
        if recipient:
            mailer.send_email(recipient, subject, html_content)
            
    elif mode == "weekly":
        weekly_insights = summarizer.generate_weekly_insights(
            {k: v["papers"] for k, v in topic_results.items()}
        )
        html_content = mailer.build_weekly_html(topic_results, weekly_insights)
        file_path = os.path.join(output_dir, f"weekly_report_{today_str}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(f"Haftalık rapor dosyası oluşturuldu: {file_path}")

        subject = f"📊 Haftalık Güç Sistemleri Trend & Tez Önerisi Raporu ({today_str})"
        if recipient:
            mailer.send_email(recipient, subject, html_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Güç Sistemleri Makale Tarama ve Raporlama Otomasyonu")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Çalıştırma modu: daily (günlük) veya weekly (haftalık)")
    args = parser.parse_args()
    
    run_pipeline(mode=args.mode)
