import argparse
import csv
import sys
from research_paper_fetcher.fetcher import PubMedFetcher
from research_paper_fetcher.parser import extract_non_academic_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers with non-academic authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file")
    
    args = parser.parse_args()

    fetcher = PubMedFetcher(email="your-email@example.com")
    pubmed_ids = fetcher.search_papers(args.query)
    papers = fetcher.fetch_paper_details(pubmed_ids)
    filtered_papers = extract_non_academic_authors(papers)

    if args.file:
        with open(args.file, mode="w", newline="", encoding="utf-8") as f:  # Add encoding="utf-8"
            writer = csv.DictWriter(f, fieldnames=filtered_papers[0].keys())
            writer.writeheader()
            writer.writerows(filtered_papers)
        print(f"Results saved to {args.file}")
    else:
        for paper in filtered_papers:
            print(paper)
if __name__ == "__main__":
    main()
