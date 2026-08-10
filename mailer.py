import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from typing import Dict, List, Any
from datetime import datetime

class Mailer:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def build_daily_html(self, topic_results: Dict[str, Dict[str, Any]]) -> str:
        """Günlük rapor için HTML e-posta gövdesi oluşturur."""
        today_str = datetime.now().strftime("%d.%m.%Y")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px; border-radius: 8px 8px 0 0; margin: -30px -30px 30px -30px; }}
                .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; }}
                .header p {{ margin: 5px 0 0 0; opacity: 0.85; font-size: 14px; }}
                .topic-title {{ color: #1e3c72; border-bottom: 2px solid #eef2f5; padding-bottom: 8px; margin-top: 30px; font-size: 18px; }}
                .paper-card {{ background: #f8fafc; border-left: 4px solid #2a5298; padding: 15px 20px; margin-bottom: 20px; border-radius: 0 6px 6px 0; }}
                .paper-title {{ font-size: 16px; font-weight: bold; color: #0f172a; text-decoration: none; margin-bottom: 5px; display: block; }}
                .paper-title:hover {{ color: #2a5298; }}
                .orig-title {{ font-size: 13px; color: #64748b; font-style: italic; margin-bottom: 8px; }}
                .meta {{ font-size: 12px; color: #475569; margin-bottom: 10px; }}
                .summary-list {{ margin: 10px 0; padding-left: 20px; font-size: 14px; line-height: 1.5; color: #334155; }}
                .key-takeaway {{ background: #e0f2fe; color: #0369a1; padding: 8px 12px; border-radius: 4px; font-size: 13px; font-weight: 500; margin-top: 10px; }}
                .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ Güç Sistemleri Günlük Akademik Yayın Raporu</h1>
                    <p>Tarih: {today_str} | Otomatik Yapay Zekâ Özeti</p>
                </div>
        """

        has_any_paper = False
        for topic_key, data in topic_results.items():
            title = data["config"]["title"]
            papers = data["papers"]
            
            html += f'<div class="topic-title">📚 {title} ({len(papers)} Yeni Makale)</div>'
            
            if not papers:
                html += '<p style="color: #64748b; font-size: 14px;">Son 48 saat içinde bu başlıkta yeni makale tespit edilmedi.</p>'
                continue

            has_any_paper = True
            for paper in papers:
                authors_str = ", ".join(paper.get("authors", [])) or "Yazar Bilgisi Yok"
                summary_items = "".join([f"<li>{s}</li>" for s in paper.get("tr_summary", [])])
                
                html += f"""
                <div class="paper-card">
                    <a class="paper-title" href="{paper['url']}" target="_blank">📌 {paper.get('tr_title', paper['title'])}</a>
                    <div class="orig-title">Orijinal: {paper['title']}</div>
                    <div class="meta">👨‍🔬 Yazarlar: {authors_str} | 📅 Tarih: {paper.get('published', '')} | 🌐 Kaynak: {paper.get('source', '')}</div>
                    
                    <div style="background: #f1f5f9; padding: 10px 15px; border-radius: 4px; font-size: 13px; color: #475569; margin-bottom: 10px; font-style: italic; border-left: 3px solid #94a3b8;">
                        <b>📖 Tam Özet (Çeviri):</b> {paper.get('tr_full_abstract', 'Özet çevirisi mevcut değil.')}
                    </div>

                    <ul class="summary-list">
                        {summary_items}
                    </ul>
                    <div class="key-takeaway">💡 <b>Önemli Katkısı:</b> {paper.get('key_takeaway', '')}</div>
                    <div class="personal-relevance" style="background: #fdf4ff; color: #a21caf; padding: 8px 12px; border-radius: 4px; font-size: 13px; font-weight: 500; margin-top: 8px; border-left: 3px solid #d946ef;">
                        🔍 <b>Araştırma Profilinizle İlişkisi:</b> {paper.get('personal_relevance', 'Analiz edilemedi.')}
                    </div>
                </div>
                """


        html += f"""
                <div class="footer">
                    <p>Bu e-posta Güç Sistemleri Otomasyon Sistemi tarafından otomatik üretilmiştir.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


    def build_weekly_html(self, topic_results: Dict[str, Dict[str, Any]], weekly_insights: Dict[str, Any]) -> str:
        """Haftalık istatistik ve tez önerisi raporu için HTML e-posta gövdesi oluşturur."""
        today_str = datetime.now().strftime("%d.%m.%Y")
        
        hot_topics_html = "".join([f"<span style='display:inline-block; background:#e2e8f0; color:#1e293b; padding:4px 10px; margin:3px; border-radius:12px; font-size:12px;'>🔥 {t}</span>" for t in weekly_insights.get("hot_topics", [])])
        
        undergrad_html = "".join([f"<li style='margin-bottom:8px;'><b>Proje Fikri:</b> {idea}</li>" for idea in weekly_insights.get("undergrad_ideas", [])])
        grad_html = "".join([f"<li style='margin-bottom:8px;'><b>Tez Konusu:</b> {idea}</li>" for idea in weekly_insights.get("grad_ideas", [])])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
                .header {{ background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%); color: white; padding: 25px; border-radius: 8px 8px 0 0; margin: -30px -30px 30px -30px; }}
                .header h1 {{ margin: 0; font-size: 22px; font-weight: 600; }}
                .section {{ margin-top: 30px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; }}
                .section-title {{ font-size: 16px; font-weight: bold; color: #0f766e; margin-bottom: 15px; border-bottom: 2px solid #ccfbf1; padding-bottom: 5px; }}
                .stat-box {{ display: flex; justify-content: space-around; background: #ffffff; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #cbd5e1; margin-bottom: 15px; }}
                .stat-num {{ font-size: 24px; font-weight: bold; color: #0f766e; }}
                .stat-label {{ font-size: 12px; color: #64748b; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Güç Sistemleri Haftalık Trend & Akademik Yönlendirme Raporu</h1>
                    <p>Tarih: {today_str} | Haftalık İstatistikler ve Tez Önerileri</p>
                </div>

                <div class="section">
                    <div class="section-title">📈 Bu Haftanın Yayın İstatistikleri</div>
                    <div style="font-size: 14px; color: #334155; margin-bottom: 15px;">
                        <b>Haftalık Genel Değerlendirme:</b> {weekly_insights.get('weekly_takeaway', '')}
                    </div>
                    <div style="margin-bottom: 15px;">
                        <b>🔥 Yükselen Popüler Konular (Hot Topics):</b><br>
                        <div style="margin-top: 8px;">{hot_topics_html}</div>
                    </div>
                </div>

                <div class="section" style="border-left: 4px solid #0284c7;">
                    <div class="section-title" style="color: #0284c7;">🎓 Lisans Öğrencileri İçin Bitirme Projesi Önerileri</div>
                    <ul style="padding-left: 20px; font-size: 14px; color: #334155;">
                        {undergrad_html}
                    </ul>
                </div>

                <div class="section" style="border-left: 4px solid #7c3aed;">
                    <div class="section-title" style="color: #7c3aed;">🔬 Lisansüstü (Yüksek Lisans / Doktora) Tez Konusu Önerileri</div>
                    <ul style="padding-left: 20px; font-size: 14px; color: #334155;">
                        {grad_html}
                    </ul>
                </div>

                <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #94a3b8;">
                    Güç Sistemleri Otomasyon Sistemi
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def send_email(self, recipient_email: str, subject: str, html_content: str):
        """E-posta gönderir."""
        if not self.sender_email or not self.sender_password:
            logging.warning("E-posta kullanıcı adı veya şifre girilmedi. Gönderim yapılmıyor.")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())

            logging.info(f"E-posta başarıyla gönderildi: {recipient_email}")
            return True
        except Exception as e:
            logging.error(f"E-posta gönderme hatası: {e}")
            return False
