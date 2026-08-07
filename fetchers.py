import arxiv
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PaperFetcher:
    def __init__(self, days_back: int = 2):
        self.cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

    def fetch_arxiv(self, query: str, max_results: int = 15) -> List[Dict[str, Any]]:
        """arXiv API üzerinden makaleleri çeker."""
        papers = []
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            for result in client.results(search):
                if result.published >= self.cutoff_date:
                    papers.append({
                        "id": result.entry_id,
                        "title": result.title.replace("\n", " ").strip(),
                        "authors": [a.name for a in result.authors],
                        "summary": result.summary.replace("\n", " ").strip(),
                        "published": result.published.strftime("%Y-%m-%d"),
                        "url": result.pdf_url or result.entry_id,
                        "source": "arXiv"
                    })
        except Exception as e:
            logging.error(f"arXiv çekme hatası: {e}")
        return papers

    def fetch_openalex(self, query: str, max_results: int = 15) -> List[Dict[str, Any]]:
        """OpenAlex API üzerinden makaleleri çeker."""
        papers = []
        try:
            url = "https://api.openalex.org/works"
            params = {
                "search": query,
                "sort": "publication_date:desc",
                "per_page": max_results
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", []):
                    # Abstract ters dizinlenmiş olabileceği için basit temizlik
                    abstract = ""
                    inv_abstract = item.get("abstract_inverted_index")
                    if inv_abstract:
                        word_list = []
                        for word, pos_list in inv_abstract.items():
                            for pos in pos_list:
                                word_list.append((pos, word))
                        word_list.sort()
                        abstract = " ".join([w[1] for w in word_list])

                    authors = []
                    for auth in item.get("authorships", []):
                        author_name = auth.get("author", {}).get("display_name")
                        if author_name:
                            authors.append(author_name)

                    doi = item.get("doi") or item.get("id")
                    title = item.get("title") or "Başlıksız Makale"

                    papers.append({
                        "id": item.get("id"),
                        "title": title.strip(),
                        "authors": authors[:5], # İlk 5 yazar
                        "summary": abstract[:1500] if abstract else "Özet bulunamadı.",
                        "published": item.get("publication_date", ""),
                        "url": doi,
                        "source": "OpenAlex"
                    })
        except Exception as e:
            logging.error(f"OpenAlex çekme hatası: {e}")
        return papers


    def fetch_for_topic(self, topic_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Bir konu için tüm kaynaklardan makaleleri toplar, özetsiz olanları eler ve tekilleştirir."""
        all_papers = []
        
        # arXiv
        arxiv_papers = self.fetch_arxiv(topic_config["arxiv_query"])
        all_papers.extend(arxiv_papers)
        
        # OpenAlex
        openalex_papers = self.fetch_openalex(topic_config["openalex_query"])
        all_papers.extend(openalex_papers)
        
        # Başlığa göre çift kayıtları temizle ve özetsiz olanları ele
        unique_papers = {}
        for paper in all_papers:
            clean_title = paper["title"].lower().strip()
            summary = paper.get("summary", "").strip()
            # Özet "Özet bulunamadı" ise veya 50 karakterden kısaysa ele
            if not summary or "Özet bulunamadı" in summary or len(summary) < 50:
                continue
            if clean_title not in unique_papers:
                unique_papers[clean_title] = paper

        return list(unique_papers.values())

