# Research Agent API

A powerful web API service for analyzing research papers using advanced AI capabilities. This service provides comprehensive analysis of academic papers in PDF format, including validity assessment, credibility analysis, and identification of potential biases.

## Features

- **PDF Analysis Endpoints**:
  - `/analyze/upload`: Process uploaded PDF files (max 16MB)
  - `/analyze/url`: Analyze PDFs from provided URLs

- **Comprehensive Analysis**:
  - Paper summaries and key findings
  - Validity assessment with confidence scores
  - Credibility analysis and citation tracking
  - Retraction status verification
  - Counter-arguments and limitations
  - Metadata extraction

## Prerequisites

- Python 3.12
- Git (for cloning with submodules)
- OpenAI API key (or compatible API like SambaNova)

## Installation

1. Clone the repository with submodules:
```bash
git clone --recursive [repository-url]
cd researchAgentAPI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.sambanova.ai/v1  # Optional: for SambaNova
OPENAI_MODEL_NAME=Meta-Llama-3.1-70B-Instruct  # Optional: specify model
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Use the API endpoints:

### Upload Endpoint
```bash
curl -X POST -F "file=@path/to/paper.pdf" http://localhost:5000/analyze/upload
```

### URL Endpoint
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/paper.pdf"}' \
     http://localhost:5000/analyze/url
```

## API Response Format

The API returns a JSON response with the following structure:
```json
{
  "analyses": {
    "summary": { "summary": "..." },
    "validity": {
      "confidence_score": 0.8,
      "validity_assessment": "..."
    },
    "credibility": {
      "citation_count": null,
      "crossref_data": null,
      "publication_info": null
    },
    "retractions": { "retraction_status": "..." },
    "counter_arguments": { "counter_arguments": "..." }
  },
  "api_usage": { "total_api_calls": 10 },
  "metadata": { ... }
}
```

## Limitations

- Maximum PDF file size: 16MB
- PDF processing might fail for complex or corrupted PDFs
- Relies on external AI API for analysis
- Limited metadata extraction capabilities

## Development

The project uses Flask for the web API and integrates with a custom ResearchAgent for paper analysis. Key components:

- `app.py`: Main Flask application with API endpoints
- `researchAgent/`: Submodule containing core research agent logic
- `.env`: Environmental configuration
- `requirements.txt`: Project dependencies

## Future Improvements

1. Enhanced error handling
2. More robust PDF parsing
3. Support for additional document formats
4. Caching mechanism for repeated analyses
5. More granular configuration options
6. Comprehensive unit and integration tests

## Security Considerations

- API key management via `.env`
- File upload size limitation
- Temporary file cleanup
- Error handling for various input scenarios

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License