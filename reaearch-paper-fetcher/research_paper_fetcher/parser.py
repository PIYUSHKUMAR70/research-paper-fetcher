from typing import List, Dict, Tuple

PHARMA_KEYWORDS = ["pharmaceutical", "biotech", "therapeutics", "biosciences"]

def extract_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Identify authors with pharma/biotech affiliations."""
    results = []
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        
        for author, aff in zip(paper["Authors"], paper["Affiliations"]):
            if aff and any(keyword in aff.lower() for keyword in PHARMA_KEYWORDS):
                non_academic_authors.append(author)
                company_affiliations.append(aff)

        results.append({
            "PubmedID": paper["PubmedID"],
            "Title": paper["Title"],
            "Publication Date": paper["Publication Date"],
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(company_affiliations)
        })
    return results
