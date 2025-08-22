# NLP Project One: Psychedelic Trip Report Analysis

## Overview
This project demonstrates natural language processing techniques for **classifying and summarizing psychedelic trip reports**. All experiments are conducted using a **Google Colab notebook** with synthetic data to illustrate preprocessing, modeling, and evaluation workflows.

## Project Goals
- **Text Classification:** Predict the category of a trip report based on its content.  
- **Abstractive Summarization:** Generate concise summaries of trip reports while preserving key experiences.  

## Notebook
**File:** `notebooks/Trip_Report_NLP_Pipeline.ipynb`  

- **Preprocessing:** tokenization, text cleaning  
- **Modeling:** Hugging Face Transformers (`AutoModelForSequenceClassification` and `AutoModelForSeq2SeqLM`)  
- **Evaluation:** classification metrics (accuracy, F1) and summarization outputs  
- Demonstrates training, evaluation, and inference on synthetic trip report data

## Dataset
- **Synthetic data** is included for reproducibility (`data/scraped/synthetic_reports.json`)  
- Original scraping methodology is discussed conceptually in the notebook, but raw scraped data is **not included** for copyright reasons  

## Dependencies
- Python 3.8+  
- `transformers`  
- `datasets`  
- `torch`  
- `evaluate`  

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Trip Report Analysis - Web Scraper Component
⚠️ Important Notice
This scraper is not functional without explicit permission from Erowid Center.
As per Erowid's robots.txt and Terms of Use, crawling and/or scraping Erowid.org requires written permission. This code is included in the repository to demonstrate:

Technical implementation of ethical web scraping
Proper project structure and error handling
Awareness of legal and ethical considerations in data collection

📋 What This Scraper Does

Implements respectful scraping with delays and user agent rotation
Handles SSL certificate issues and connection errors
Extracts structured data from trip report pages
Saves data in multiple formats (JSON, CSV)
Includes comprehensive logging and error handling

🛠️ Technical Features
Ethical Scraping Practices

Respects robots.txt guidelines
Implements random delays between requests
Uses proper user agent headers
Includes rate limiting and timeout handling

Data Extraction

Parses HTML using BeautifulSoup4
Handles dynamic content between HTML comments
Extracts structured fields (substance, dosage, experience text, etc.)
Validates data quality before saving

Error Handling

SSL certificate verification handling
Network timeout and retry logic
Graceful degradation with fallback URLs
Comprehensive logging for debugging
