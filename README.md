# Browser Automation & Rendering Service

FastAPI-based browser automation service for rendering JavaScript-heavy web platforms, handling authenticated sessions, and returning cleaned XHTML/text output for downstream scraping and data-processing pipelines.

The service was developed as a core rendering component within larger multi-source patent marketplace extraction workflows involving authenticated TIPX/IAM platforms and dynamic client-side rendered applications.

## Features

- Full JavaScript rendering using Playwright
- Automated authenticated session handling
- Configurable credential-based login workflows
- XHTML and plain-text extraction
- HTML cleaning and normalization
- Removal of scripts, styles, forms, and navigation elements
- Async FastAPI service architecture
- Stealth browser automation support
- Structured JSON response generation
- Designed for integration into large scraping pipelines

## Tech Stack

- Python
- FastAPI
- Playwright
- playwright-stealth
- BeautifulSoup4
- Pydantic
- AsyncIO

## Architecture

```text
Target Platform Request
            ↓
Headless Chromium Launch
            ↓
Authentication Workflow
            ↓
Dynamic Page Rendering
            ↓
HTML Extraction
            ↓
Content Cleaning & Normalization
            ↓
Structured XHTML/Text Output
            ↓
Downstream Parsing Pipelines
```

## Project Structure

```text
tipx-browser-automation/
│
├── app.py
├── config.json
├── requirements.txt
└── README.md
```

## Key Components

- Async Playwright browser automation engine
- Authentication/session management workflows
- HTML cleaning and normalization utilities
- XHTML/text extraction pipeline
- FastAPI API service layer
- Structured response generation
- Configurable platform integration logic

## API Endpoint

### POST `/fetch_text`

Fetches a fully rendered page, processes the content, and returns cleaned XHTML and plain text.

## Notes

Designed for dynamic platform rendering, authenticated data extraction workflows, and preprocessing of JavaScript-heavy web applications prior to structured parsing and storage.

The service was used as part of larger automated scraping infrastructure responsible for tracking and processing marketplace listings across multiple patent-related platforms.
