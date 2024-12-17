# Arxiv Paper Summarizer

A web application to fetch and translate summaries from Arxiv.org papers using GPT-3.5.

## Features

- Modern and responsive web interface
- Paper search by category
- Automatic translation of titles and summaries
- PDF preview
- Minimalist design with TailwindCSS

## Requirements

- Python 3.13
- OpenAI API Key

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the server:
   ```bash
   python main.py
   ```
2. Open in browser: `http://localhost:5000`

### Web Interface

The web interface allows you to:
- Select the paper category to search
- Specify the number of results
- View paper summaries with a clean and modern design
- Get translations with a single click
- Access paper PDFs directly

### API Endpoints

You can also use the API directly:

1. **GET /papers/**
   - Gets recent papers from Arxiv
   - Parameters:
     - `category` (optional): Arxiv category (default: "cs.AI")
     - `max_results` (optional): Maximum number of results (default: 5)
   - Example: `http://localhost:5000/papers/?category=cs.AI&max_results=3`

2. **GET /papers/<paper_id>/summary**
   - Gets a translated summary of a specific paper
   - Parameters:
     - `translate` (optional): Whether to translate the title (default: true)
   - Example: `http://localhost:5000/papers/2312.01047/summary`

## API Response Example

```json
{
    "original_title": "Deep Learning in Computer Vision",
    "translated_title": "Deep Learning in Computer Vision",
    "original_summary": "This paper presents...",
    "translated_summary": "This paper presents..."
}
