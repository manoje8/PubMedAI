import time
from typing import List, Dict, Optional

import requests
from Bio import Entrez, Medline

from config import Config


class PubMedFetcher:
    def __init__(self):
        Entrez.email = Config.PUBMED_EMAIL
        Entrez.api_key = Config.PUBMED_API_KEY


    def search_articles(self, query: str, max_result:int = 20) -> List[str]:
        """Search PubMed for articles matches the query"""

        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_result,
                sort="relevance",
            )

            records = Entrez.read(handle)
            handle.close()

            return records["IdList"]

        except Exception as e:
            print(f"Error searching PubMed for {e}")
            return []

    def fetch_article_details(self, pubmed_ids: List[str]) -> List[Dict]:

        articles = []

        for i in range(0, len(pubmed_ids), 100):
            batch_ids = pubmed_ids[i : i+100]

            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    id=batch_ids,
                    rettype="medline",
                    retmode="text",
                )

                records = Medline.parse(handle)

                print("RECORDS", records)

                #TODO: Check and add it the records

                for record in records:
                    article = {
                        "pmid": record.get("PMID", ""),
                        "title": record.get("TI", ""),
                        "abstract": record.get("AB", ""),
                        "authors": record.get("AU", []),
                        "journal": record.get("TA", ""),
                        "publication_date": record.get("DP", ""),
                        "mesh_terms": record.get("MH", []),
                        "doi": record.get("LID", "").replace(" [doi]", "") if ['doi'] in record.get("LID", "") else None,
                    }

                    articles.append(article)

                handle.close()
                time.sleep(0.34) # NCBI rate limits

            except Exception as e:
                print("Error in fetch_article_details: {}".format(e))

        def download_full_text(self, article: Dict) -> Optional[str]:
            """Download the full text of the article if present"""

            if article.get("doi"):
                try:
                    url = f"https://doi.org/{article['doi']}"
                    response = requests.get(url, headers={"Accept": "text/plain"})

                    if response.status_code == 200:
                        return response.text
                except:
                    pass


            return article.get("abstract", "")