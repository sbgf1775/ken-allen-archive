# The Ken Allen Archive
### A Computational Research Interface for PLA Studies
**GLBL 5050 Final Project | Anthony Costanzo | Samuel B. Griffith Foundation for Chinese Military Studies**

---

## Live Application

**[Ken Allen Archive — Launch App](https://ken-allen-archive.streamlit.app)**

Hosted on Streamlit Community Cloud. No login required. Works on any device.

---

## What This Project Does

This project builds a functional research interface for the Kenneth Allen Archive — over 2,000 documents
representing decades of original scholarship, translated primary sources, and analysis on the People's
Liberation Army (PLA), held in the Samuel B. Griffith Foundation's Google Drive. Kenneth W. Allen is
one of the foremost Western authorities on PLA organization, personnel, and airpower.

Before this project, finding a specific document required manually navigating folder structures with no
search capability and no subject tagging. This project turns that filing cabinet into a searchable,
queryable, and visually navigable research interface — publicly accessible for the first time.

---

## Project Evolution

The original project proposed scraping PLA state media (81.cn) to analyze robotics coverage trends.
It failed because modern Chinese government websites render content dynamically via JavaScript, making
their archives programmatically inaccessible despite five distinct technical approaches including
Selenium, Playwright, and API probing. The pivot reoriented toward a richer, more tractable data source
— a curated archive in a cloud environment designed for programmatic access. Both projects apply
identical computational methods to the same substantive domain. The difference is that this one closes end to end.

---

## Technical Pipeline

### Circle 1 — Authentication & Indexing
- OAuth 2.0 authentication to Google Drive API
- Recursive enumeration of 2,064 files across 25 subject folders
- Saves `ken_allen_index.csv`

### Circle 2 — Extraction, Scoring & Detection
- **Text extraction** — PyMuPDF for PDFs, python-docx for Word files; 1,683 readable documents processed
- **Tokenization** — NLTK stop word removal and `collections.Counter` — top 5 keywords per document
- **Custom dictionary scoring** — 10-category PLA subject vocabulary scores each document by dominant topic
- **Sentiment analysis** — VADER compound score applied across full corpus (avg: 0.37)
- **Draft detection** — filename and content signals flag 217 working documents; excluded from public interface
- **Year extraction** — regex pulls most recent 4-digit year (1980-2026) from filename
- Saves `ken_allen_scored.csv` — 1,160 documents scored, 943 publicly available

### Circle 3 — Maintenance
- Incremental update: process only new files not already in scored CSV
- Snippet refresh: re-download and update text snippets without re-scoring

---

## Application Features

### Search Mode
- Keyword search ranked by term frequency across filename, snippet, and keyword fields
- Rotating placeholder suggestions using session_state
- Top 25 results with topic, sentiment, keywords, 1,500-character snippet, and direct Google Drive link

### Browse Mode
- Filter by subject folder (24 folders), PLA topic (10 categories), and publication year
- Year slider (1981-2024) with toggle gate
- Topic distribution bar chart and documents-by-folder table

### Insights & Network — Analytics Tab
1. **Research Focus Over Time** — stacked area chart of document volume by topic and year (1991-2024)
2. **Top Keywords by Research Topic** — horizontal bar chart of distinctive vocabulary per topic
3. **Topic Concentration Heatmap** — normalized folder x topic matrix
4. **Archive Structure Treemap** — full archive hierarchy by folder and topic, clickable and zoomable
5. **Leadership Mentions Over Time** — named leader mentions normalized per 100 docs, with event annotations and summary table

### Insights & Network — Network Graph Tab
- Interactive pyvis network: documents as nodes, keyword overlap as edges
- Nodes colored by PLA topic; hover tooltip includes title, topic, keywords, and Drive link
- Filters: topic, max documents (25-150), minimum shared keywords (1-4)

---

## Course Concepts Applied

| Concept | Application |
|---|---|
| API & Data Retrieval | Google Drive OAuth 2.0 — recursive folder enumeration |
| Text Processing | PyMuPDF + python-docx across 1,683 documents |
| Frequency Distribution | collections.Counter — top 5 keywords per document |
| Custom Dictionary | 10 PLA topic categories — extends HW4 methodology |
| Sentiment Analysis | VADER across full corpus — avg compound score 0.37 |
| OOP Design | Document indexing pipeline — HW5 class structure |
| Data Storage | pandas DataFrame + reproducible CSV |
| Visualization | Plotly stacked area, bar, heatmap, treemap; pyvis network graph |
| Streamlit | Search, browse, analytics, network — four-mode interface |

---

## Repository Structure

    ken-allen-archive/
    |-- ken_allen_app.py          # Streamlit application
    |-- ken_allen_scored.csv      # 1,160 scored documents (943 public)
    |-- ken_allen_photo.webp      # Kenneth W. Allen photo
    |-- sbgf_logo.webp            # SBGF logo
    |-- requirements.txt          # Python dependencies
    |-- .gitignore                # Excludes credentials and notebooks

**Not included in repo (local only):**
- credentials.json — OAuth client secret
- token.pickle — Drive authentication token
- Archive_Pipeline_Final.ipynb — extraction pipeline notebook
- Streamlit_App_Final.ipynb — app notebook

---

## Contact & Citation

**Samuel B. Griffith Foundation for Chinese Military Studies**
sbgfoundation@protonmail.com

*Materials graciously provided by Kenneth W. Allen, Advisor Emeritus.*

When referencing materials from this archive, please cite the original document and author directly.
Example: Allen, Kenneth W. [Document Title]. Samuel B. Griffith Foundation for Chinese Military
Studies Archive. Retrieved from https://ken-allen-archive.streamlit.app

© 2026 Samuel B. Griffith Foundation for Chinese Military Studies. All rights reserved.