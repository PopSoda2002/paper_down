# Paper Down

A simple tool to download papers from Google Scholar profiles.

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/paper_down.git
cd paper_down
```

2. Install required dependencies:
```
pip install requests beautifulsoup4 scholarly tqdm
```

## Usage

Run the script with a Google Scholar profile URL:

```
python paper_down.py "https://scholar.google.com/citations?user=SCHOLAR_ID"
```

### Options

- `--output_dir`: Specify the directory to save papers (default: ./papers)
- `--limit`: Maximum number of papers to download (default: 10)

### Examples

Download papers to the default directory:
```
python paper_down.py "https://scholar.google.com/citations?user=SCHOLAR_ID"
```

Download papers to a custom directory:
```
python paper_down.py "https://scholar.google.com/citations?user=SCHOLAR_ID" --output_dir ~/my_papers
```

Download 20 papers instead of the default 10:
```
python paper_down.py "https://scholar.google.com/citations?user=SCHOLAR_ID" --limit 20
```

## Features

- Downloads papers from a Google Scholar profile
- Sorts papers by citation count (most cited first)
- Skips already downloaded papers
- Shows progress bar during download
- Handles different paper sources and formats

## Notes

- The tool sorts papers by citation count and downloads the most cited ones first
- PDFs are saved using the paper title as the filename
- Already downloaded papers are skipped
- The script includes a delay between downloads to avoid being blocked by Google 