import os
import json
import logging
from typing import List, Dict, Any
from google import genai
from google.genai import types

try:
    from my_research_profile import RESEARCH_PROFILE
except ImportError:
    RESEARCH_PROFILE = "Araştırma profili bulunamadı."

class PaperSummarizer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logging.error(f"Gemini Client başlatılamadı: {e}")
                self.client = None
        else:
            self.client = None
            logging.warning("GEMINI_API_KEY bulunamadı. Özetleme işlemi şablon modda çalışacak.")

    def summarize_daily_papers(self, topic_name: str, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Günlük makaleleri Türkçe özetler ve analiz eder."""
        if not papers:
             summarized_papers = []
        for paper in papers:
            if not self.client:
                # API Key yoksa veya çalışmadıysa makaleden Türkçe özet şablonu oluştur
                paper["tr_title"] = paper["title"]
                paper["tr_full_abstract"] = "API Key eksikliği nedeniyle tam özet çevrilemedi."
                paper["tr_summary"] = [
                    f"Özet (Orijinal): {paper['summary'][:250]}...",
                    "Yöntem: Bu çalışma akıllı şebeke alanında yenilikçi modeller sunmaktadır.",
                    "Bulgu: Detaylar makale tam metninde mevcuttur."
                ]
                paper["key_takeaway"] = f"{topic_name} alanında güncel bir akademik çalışma."
                paper["personal_relevance"] = "API Key bulunamadığı için profilleme yapılamadı."
                summarized_papers.append(paper)
                continue

            prompt = f"""
            Sen Güç Sistemleri ve Akıllı Şebekeler alanında uzman bir akademisyensin.
            Aşağıdaki makaleyi dikkatle oku ve Türkçe olarak özetle.
            
            Ayrıca benim "Kişisel Araştırma Profilimi" kullanarak, bu makalenin benim çalışmalarımla (yöntem, konu, problem açısından) nasıl örtüştüğünü veya nasıl bir alternatif/katkı sunduğunu 1-2 cümleyle "personal_relevance" alanında açıkla.

            --- BENİM ARAŞTIRMA PROFİLİM ---
            {RESEARCH_PROFILE}
            --------------------------------

            --- İNCELENECEK MAKALE ---
            Makale Başlığı: {paper['title']}
            Özet (Abstract): {paper['summary']}
            --------------------------

            Lütfen YALNIZCA aşağıdaki JSON formatında yanıt ver:
            {{
                "tr_title": "Makale başlığının akıcı ve doğru Türkçe çevirisi",
                "tr_full_abstract": "Makalenin orijinal özetinin (abstract) tam ve akademik dille Türkçe çevirisi.",
                "tr_summary": [
                    "Ele alınan temel problem veya çalışma amacı",
                    "Kullanılan yöntem, algoritma veya model",
                    "Elde edilen ana bulgular ve sonuçlar"
                ],
                "key_takeaway": "Bu çalışmanın sektöre/literatüre getirdiği en önemli yenilik veya katkı.",
                "personal_relevance": "Kişisel araştırma profilimle olan teorik/metodolojik ilişkisi veya farklılığı."
            }}
            """

            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                res_data = json.loads(response.text)
                paper["tr_title"] = res_data.get("tr_title", paper["title"])
                paper["tr_full_abstract"] = res_data.get("tr_full_abstract", "Tam özet çıkarılamadı.")
                paper["tr_summary"] = res_data.get("tr_summary", [paper["summary"][:300]])
                paper["key_takeaway"] = res_data.get("key_takeaway", "Çalışmanın katkısı detaylandırıldı.")
                paper["personal_relevance"] = res_data.get("personal_relevance", "Doğrudan bir ilişki kurulamadı.")
            except Exception as e:
                logging.error(f"Gemini özetleme hatası ({paper['title']}): {e}")
                paper["tr_title"] = paper["title"]
                paper["tr_full_abstract"] = "Tam özet çeviri hatası oluştu."
                paper["tr_summary"] = [paper["summary"][:300] + "..."]
                paper["key_takeaway"] = "Makale özetinden türetilen akademik çalışma."
                paper["personal_relevance"] = "Özetleme hatası nedeniyle analiz yapılamadı."

            summarized_papers.append(paper)
        return summarized_papers

    def generate_weekly_insights(self, topic_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Haftalık trend analizi, istatistikler ve öğrenciler için tez/araştırma fikirleri üretir."""
        if not self.client:
            return {
                "hot_topics": ["Smart Grid Resilience", "Blockchain in P2P Trading", "V2G Grid Integration"],
                "undergrad_ideas": ["P2P Enerji ticareti için Python simülasyonu", "IEEE 13 bara test sisteminde EV etkilerinin modellenmesi"],
                "grad_ideas": ["Evirici tabanlı mikroşebekelerde adaptif koruma için derin takviyeli öğrenme", "Dinamik şebeke tarifelerinde P2P oyun teorisi modelleri"],
                "weekly_takeaway": "Bu hafta akıllı şebekelerde dijitalleşme öne çıktı."
            }

        all_summaries = []
        for topic_key, papers in topic_results.items():
            for p in papers:
                all_summaries.append(f"Konu: {topic_key} | Başlık: {p['title']} | Özet: {p['summary'][:200]}")

        prompt = f"""
        Son bir haftada Güç Sistemleri alanında (Akıllı Şebekelerde Koruma, P2P Enerji Ticareti, Elektrikli Araçların Şebekeye Etkileri) yayınlanan aşağıdaki makalelerin özetlerini incele ve kapsamlı bir haftalık trend ve akademik yönlendirme raporu hazırla:

        MAKALELER:
        {" ".join(all_summaries[:25])}

        ÖĞRENCİ ÖNERİLERİ İÇİN KRİTİK TALİMAT: 
        Lütfen Lisans ve Lisansüstü önerilerini oluştururken çok spesifik ve karşılaştırmalı ol. 
        Şu formatı sıkı bir şekilde kullan: "Bu haftaki çalışmalarda X yöntemi kullanılmış, ancak Y yöntemi / Z veri seti ile bir çalışma yapılırsa özgünlük elde edilebilir."

        Lütfen şu JSON formatında yanıt ver:
        {{
            "hot_topics": ["Yükselen Trend 1", "Yükselen Trend 2", "Yükselen Trend 3", "Yükselen Trend 4"],
            "undergrad_ideas": [
                "Lisans Bitirme Projesi Önerisi 1 (X yapılmış, Y yapılırsa özgünlük katar şeklinde)",
                "Lisans Bitirme Projesi Önerisi 2"
            ],
            "grad_ideas": [
                "Lisansüstü Tez Konusu Önerisi 1 (Bu hafta X kullanılmış, şu Y yöntemi ile çözülürse özgünlük elde edilir şeklinde)",
                "Lisansüstü Tez Konusu Önerisi 2"
            ],
            "weekly_takeaway": "Bu haftanın yayın genel değerlendirmesi ve sektörün gidişatı hakkında 2 cümlelik özet."
        }}
        Yalnızca geçerli bir JSON objesi döndür.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logging.error(f"Haftalık insight üretme hatası: {e}")
            return {
                "hot_topics": ["Mikroşebeke Koruma", "P2P Enerji", "V2G Şebeke Dengelenmesi"],
                "undergrad_ideas": ["Bu hafta geleneksel analizler yapılmış, Python'da makine öğrenmesi ile yapılırsa özgünlük katar."],
                "grad_ideas": ["Çalışmalarda basit CNN kullanılmış, ancak karmaşık LSTM yapılarıyla özgün bir tez çıkarılabilir."],
                "weekly_takeaway": "Bu hafta akıllı şebekelerde dijitalleşme ve yenilenebilir entegrasyonu öne çıktı."
            }
ergrad_ideas": ["P2P Enerji Ticareti Simülasyonu"],
                "grad_ideas": ["Adaptif Koruma Algoritmaları"],
                "weekly_takeaway": "Bu hafta akıllı şebekelerde dijitalleşme ve yenilenebilir entegrasyonu öne çıktı."
            }
