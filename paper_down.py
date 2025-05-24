#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from scholarly import scholarly
import time
from tqdm import tqdm

def download_papers_from_scholar(scholar_url, output_dir, limit=10):
    """
    Download the top k papers from a Google Scholar profile to a specified directory.
    
    Args:
        scholar_url (str): URL of the Google Scholar profile
        output_dir (str): Directory to save the downloaded papers
        limit (int): Maximum number of papers to download
    
    Returns:
        list: List of successfully downloaded paper titles
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract author ID from URL
    parsed_url = urllib.parse.urlparse(scholar_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    user_id = query_params.get('user', [None])[0]
    
    if not user_id:
        raise ValueError("Could not extract author ID from Google Scholar URL")
    
    print(f"Fetching publications for author ID: {user_id}")
    
    # Get author data using scholarly
    author = scholarly.search_author_id(user_id)
    scholarly.fill(author, sections=['publications'])
    
    # Get publications
    publications = author['publications']
    downloaded_papers = []
    
    # Sort by citation count (most cited first)
    publications = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)
    
    # Process only the top k papers
    for i, pub in enumerate(publications[:limit]):
        if i >= limit:
            break
            
        # Fill publication details
        try:
            scholarly.fill(pub)
            title = pub.get('bib', {}).get('title', f"paper_{i}")
            print(f"\nProcessing [{i+1}/{limit}]: {title}")
            
            # Clean filename
            safe_title = re.sub(r'[^\w\-_\. ]', '_', title)
            safe_title = safe_title[:100]  # Truncate long titles
            filename = os.path.join(output_dir, f"{safe_title}.pdf")
            
            # Skip if already downloaded
            if os.path.exists(filename):
                print(f"Paper already exists: {filename}")
                downloaded_papers.append(title)
                continue
                
            # Try to get PDF URL
            pdf_url = None
            if 'pub_url' in pub:
                # Try to find PDF link from publication page
                try:
                    response = requests.get(pub['pub_url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Look for PDF links
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            if href.endswith('.pdf') or 'pdf' in href.lower():
                                pdf_url = href if href.startswith('http') else urllib.parse.urljoin(pub['pub_url'], href)
                                break
                except Exception as e:
                    print(f"Error fetching publication page: {e}")
            
            # If direct PDF not found, try alternative sources
            if not pdf_url and 'eprint_url' in pub:
                pdf_url = pub['eprint_url']
            
            # Download PDF if URL found
            if pdf_url:
                try:
                    print(f"Downloading from: {pdf_url}")
                    response = requests.get(pdf_url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=60)
                    
                    # Check if it's a PDF
                    content_type = response.headers.get('Content-Type', '').lower()
                    if response.status_code == 200 and ('application/pdf' in content_type or pdf_url.endswith('.pdf')):
                        # Download with progress bar
                        total_size = int(response.headers.get('content-length', 0))
                        with open(filename, 'wb') as f, tqdm(
                                total=total_size,
                                unit='B',
                                unit_scale=True,
                                unit_divisor=1024,
                                desc=safe_title[:30]
                            ) as bar:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                                    bar.update(len(chunk))
                        
                        print(f"Successfully downloaded: {filename}")
                        downloaded_papers.append(title)
                    else:
                        print(f"Failed to download PDF. Invalid content type: {content_type}")
                except Exception as e:
                    print(f"Error downloading PDF: {e}")
            else:
                print(f"Could not find PDF link for: {title}")
                
        except Exception as e:
            print(f"Error processing publication: {e}")
        
        # Add delay to avoid being blocked
        time.sleep(2)
    
    # Summary
    print(f"\nDownloaded {len(downloaded_papers)}/{limit} papers to {output_dir}")
    return downloaded_papers

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download papers from Google Scholar")
    parser.add_argument("scholar_url", help="URL of the Google Scholar profile")
    parser.add_argument("--output_dir", default="./papers", help="Directory to save the downloaded papers (default: ./papers)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of papers to download (default: 10)")
    
    args = parser.parse_args()
    
    download_papers_from_scholar(args.scholar_url, args.output_dir, args.limit) 