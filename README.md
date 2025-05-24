# Paper Down

A simple tool to download papers from Google Scholar profiles. It automatically fetches the most cited papers from a researcher's profile and attempts to download the PDFs.

## Installation

1. Clone this repository:
```
git clone https://github.com/PopSoda2002/paper_down.git
cd paper_down
```

2. Install required dependencies:
```
pip install requests beautifulsoup4 scholarly tqdm
```

## How to Find Google Scholar ID

1. Go to the researcher's Google Scholar profile page
2. The URL will look like: `https://scholar.google.com/citations?user=SCHOLAR_ID`
3. Copy the SCHOLAR_ID value (a string like HQqQ6OIAAAAJ)

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

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'scholarly'**
   - Make sure you've installed all dependencies: `pip install scholarly`

2. **Cannot find PDF links**
   - Not all papers have publicly accessible PDFs
   - Some publishers restrict access to PDFs

3. **Google Scholar blocking requests**
   - The script includes delays to avoid being blocked, but if you make too many requests, Google might temporarily block your IP
   - Try again later or use a VPN

## License

This project is open source and available under the MIT License. 