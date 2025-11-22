# Legislative AI Agent

A Python application that processes legislation PDFs using Google Gemini API to extract structured insights and generate compliance reports.

## Workflow

![Legislative AI Agent Workflow](assets/workflow.png)

## Project Structure

```
/project_root
│
├── agent.py              # Main LegislativeAgent class (orchestrator)
├── app.py                # Streamlit UI application
├── debug_agent.py        # Debug script for the agent
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── assets/               # Asset files
│   └── workflow.png      # Workflow diagram
├── output/               # Output files
│   ├── chunk_summaries.json  # Intermediate chunk summaries
│   └── legislation_analysis.json  # Final output
└── src/                  # Source modules
    ├── __init__.py
    ├── text_utils.py         # Text extraction, cleaning, and chunking utilities
    ├── summarizer.py         # Text summarization functionality
    ├── section_extractor.py  # Section extraction from legislation
    ├── rule_checker.py       # Legal document rule compliance checking
    └── json_exporter.py      # JSON export functionality
```

## Detailed Implementation Overview

This Legislative AI Agent was developed using Python 3.12 and follows a comprehensive workflow to process legal documents. The implementation focuses on modularity, efficiency, and accuracy in analyzing legislation PDFs.

### Core Workflow Implementation

#### 1. PDF Text Ingestion and Preprocessing
The process begins with uploading a legislation PDF through the Streamlit UI. The system uses PyMuPDF (fitz) to extract raw text from the PDF document. Advanced text cleaning techniques are applied to remove common artifacts:
- Page numbers and page indicators ("Page X of Y")
- Excessive whitespace and blank lines
- Isolated numbers (typically page numbers)
- Non-ASCII characters that might cause processing issues
- Text normalization for consistent formatting

#### 2. Intelligent Text Chunking
To handle large legal documents effectively, the cleaned text is split into manageable chunks:
- Default chunk size: 6000 characters
- Overlapping prevented to maintain context integrity
- Chunk boundaries respect word boundaries when possible
- This approach enables processing of documents of any length while staying within LLM context limits

#### 3. Parallel Chunk Processing
Each text chunk is processed independently to maximize efficiency:
- Individual chunk summarization using Google Gemini 2.5 Flash model
- Section extraction from the complete text
- Rule compliance checking against legal document standards
- Parallel processing capabilities for performance optimization

#### 4. Hierarchical Summarization
The summarization process follows a two-tier approach:
- **First Level**: Each chunk is summarized independently into 3-4 bullet points
- **Second Level**: All chunk summaries are combined into a comprehensive final summary covering:
  - Purpose of the legislation
  - Key definitions
  - Eligibility criteria
  - Obligations and responsibilities
  - Enforcement mechanisms

#### 5. Schema-Based Section Extraction
The system extracts specific sections from the legislation following a predefined schema:
- Definitions
- Obligations
- Responsibilities
- Eligibility
- Payments
- Penalties
- Record-keeping

This structured extraction ensures consistent output format regardless of input document variations.

#### 6. Legal Document Rule Compliance Checking
The agent validates the legislation against 6 critical legal document rules:
1. **Key Terms Definition**: Verifies if the act defines essential terminology
2. **Eligibility Criteria**: Checks if the act specifies who qualifies
3. **Authority Responsibilities**: Determines if government obligations are defined
4. **Enforcement Methods**: Verifies if penalties or enforcement mechanisms are listed
5. **Payment Calculations**: Checks if payment methodologies are explained
6. **Record-keeping Requirements**: Determines if reporting obligations exist

For each rule, the system provides:
- Pass/fail status
- Evidence excerpt from the text
- Confidence score (0-100)

#### 7. Data Storage and JSON Export
Results are systematically stored in structured JSON formats:

**Intermediate Storage**:
- `output/chunk_summaries.json`: Contains individual chunk summaries for audit and reuse
- Optimized to avoid reprocessing when the same document is analyzed multiple times

**Final Output** (`output/legislation_analysis.json`):
```json
{
  "summary": "Final comprehensive summary...",
  "sections": {
    "definitions": "...",
    "obligations": "...",
    "responsibilities": "...",
    "eligibility": "...",
    "payments": "...",
    "penalties": "...",
    "record_keeping": "..."
  },
  "rule_checks": [
    {
      "rule": "Act must define key terms",
      "status": "pass/fail",
      "evidence": "Specific text excerpt...",
      "confidence": 95
    }
  ],
  "chunk_summaries": ["...", "..."]
}
```

### Technical Architecture

#### Modular Design
The system follows a modular architecture with separate components:
- **Text Utilities**: Handles PDF extraction, cleaning, and chunking
- **Summarizer**: Manages hierarchical text summarization
- **Section Extractor**: Performs schema-based section extraction
- **Rule Checker**: Implements legal document compliance validation
- **JSON Exporter**: Manages structured data storage

#### AI Model Configuration
- **Primary Model**: Google Gemini 2.5 Flash
- **Temperature Setting**: 0.3 (optimized for stable, consistent responses)
- **Reasoning**: Lower temperature reduces hallucinations in legal document analysis

#### Performance Optimizations
- Chunk summary caching to avoid redundant processing
- Structured logging for debugging and monitoring
- Efficient memory management for large document processing

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   or if using python3:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Set Google API Key**:
   Create a `.env` file in the project root with your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   
   Alternatively, you can enter the API key in the Streamlit UI.

3. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

## Features

- **Modular Design**: Each component is separated into its own module for maintainability
- **PDF Upload**: Upload any legislation PDF for analysis
- **Text Extraction**: Extract and clean text from PDFs with advanced cleaning
- **AI Processing**: Process legislation with Google Gemini 2.5 Flash model
- **Executive Summary**: Bullet-point summary of key provisions
- **Section Extraction**: Isolated views of definitions, obligations, etc.
- **Legal Document Compliance Checking**: Rule validation against 6 specific legal document rules
- **Chunk Storage**: Individual chunk summaries are stored for audit purposes
- **JSON Export**: Download structured analysis reports
- **Optimized Processing**: Reuses existing chunk summaries if available

## Requirements

- Python 3.12
- Google Gemini API key
- Dependencies listed in requirements.txt

## No External Libraries

This implementation avoids external libraries like:
- LangChain
- RAG systems
- Embedding models

All processing is done directly with the Google Generative AI SDK.

## Advanced Text Cleaning

The agent now includes advanced text cleaning features:
- Removal of page numbers and artifacts
- Normalization of whitespace
- Elimination of isolated numbers
- Removal of non-ASCII characters
- Consolidation of multiple blank lines

## Chunk Processing

Each text chunk is processed individually and stored:
- Chunk summaries are saved for audit purposes
- Individual processing allows for better handling of large documents
- Results can be reviewed at each step of the pipeline
- Existing chunk summaries are reused to save processing time

## Legal Document Rule Compliance

The agent checks legislation against 6 specific legal document rules:
1. **Key Terms Definition**: Verifies if the act defines key terms
2. **Eligibility Criteria**: Checks if the act specifies who is eligible
3. **Authority Responsibilities**: Determines if the act specifies what the government must do
4. **Enforcement Methods**: Verifies if the act lists penalties or enforcement methods
5. **Payment Calculations**: Checks if the act explains how to calculate payments
6. **Record-keeping Requirements**: Determines if the act requires records or reporting

For each rule, the agent determines:
- Pass/fail status
- Evidence from the text
- Confidence score (0-100)

## Model Configuration

The agent uses the Google Gemini 2.5 Flash model with a temperature of 0.3 for more stable responses.