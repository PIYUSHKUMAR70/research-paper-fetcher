import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

class PubMedFetcher:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, email: str):
        self.email = email

    def search_papers(self, query: str, max_results: int = 10) -> List[str]:
        """Fetch PubMed IDs based on query."""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
            "email": self.email
        }
        response = requests.get(self.BASE_URL, params=params)
        root = ET.fromstring(response.content)
        return [id_elem.text for id_elem in root.findall(".//Id")]

    def fetch_paper_details(self, pubmed_ids: List[str]) -> List[Dict[str, Optional[str]]]:
        """Fetch detailed metadata for given PubMed IDs."""
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "retmode": "xml",
            "email": self.email
        }
        response = requests.get(self.FETCH_URL, params=params)
        root = ET.fromstring(response.content)

        papers = []
        for article in root.findall(".//PubmedArticle"):
            pubmed_id = article.find(".//PMID").text
            title = article.find(".//ArticleTitle").text
            date = article.find(".//PubDate").text
            authors = [
                author.find(".//LastName").text for author in article.findall(".//Author")
            ]
            affiliations = [
                aff.text for aff in article.findall(".//Affiliation")
            ]
            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": date,
                "Authors": authors,
                "Affiliations": affiliations
            })
        return papers
