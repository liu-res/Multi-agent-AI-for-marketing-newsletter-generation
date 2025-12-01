# Multi-agent for Marketing Newsletter Generation

A multi-agent AI system that automatically generates HTML newsletters by extracting product insights, researching industry trends, and creating email-ready EDM designs.

## Description

This system uses Google's Agent Development Kit (ADK) to orchestrate multiple specialized AI agents that work together to:

1. **Collect Internal Data**: Extract key selling points from product documentation (PDFs)
2. **Find External Trends**: Research latest industry trends and developments
3. **Write Content**: Synthesize internal insights and external trends into compelling newsletter content
4. **Design HTML**: Transform content into a professionally designed, email-ready HTML newsletter


## Workflow Modes

**Full Generation Mode** (when `newsletter_content.txt` doesn't exist):
1. Data_Collection_Agent reads PDFs from `product_data/`
2. Trend_Finding_Agent searches for industry trends
3. Content_Writing_Agent creates newsletter content
4. Visual_Design_Agent creates HTML newsletter

**Design-Only Mode** (when `newsletter_content.txt` exists):
1. Visual_Design_Agent reads existing content
2. Creates HTML newsletter directly


## Project Directory

```
newsletter_automation/
├── agent.py                          # Main agent definitions and orchestration
├── prompts.py                        # Agent prompts and instructions
│
├── func_tools/                       # Function tools and MCP servers
│   ├── mcp_pdf_reader.py            # PDF reading via MCP server
│   ├── mcp_html_reader.py           # HTML file reading tools
│   ├── mcp_image_gen.py             # Image generation (optional)
│   └── newsletter_file_tools.py     # File operations (read/write/check)
│
├── product_data/                    # Input: Product documentation
│   └── Mock_Product_Data.pdf        # Example product data PDF
│
├── style_samples/                    # Input: HTML newsletter templates
│   ├── Sample_Style_Template/        # Sample template with images
│   │   ├── Sample_Newsletter_Template.html
│   │   └── images/                  # Template images
│   └── [other style samples]/       # Additional style references
│
├── output/                          # Output: Generated files
│   ├── newsletter_content.txt       # Generated newsletter text content
│   ├── newsletter.html              # Final HTML newsletter
│   └── images/                       # Newsletter images (if generated)
│
└── README.md                        # This file
└── ...
```

## Requirements

### Python Version
- Python 3.8 or higher

### API Keys
- **GOOGLE_API_KEY**: Required for Google Gemini API access
  - Get your API key from: https://ai.google.dev/
  - Set it in `.env` file or as an environment variable


## Usage

### 1. Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install google-adk python-dotenv

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 2. Prepare Your Data - Bring Your Own Product Details and Style Templates

#### Adding Product Data

Place PDF files in the `product_data/` directory:
```bash
cp your_product_documentation.pdf product_data/
```

#### Style Samples
Add HTML newsletter templates to `style_samples/` for design inspiration:
```bash
### Example Style Sample Structure
style_samples/MyBrandStyle/
├── MyBrandStyle.html          # Your HTML template
└── images/
    ├── logo.png              # Company logo
    ├── hero.jpg              # Hero image
    └── icon1.png             # Feature icons
```

### 3. Run the Agent

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the newsletter generation
python3 agent.py
```

### 4. Output

The system will generate:
- `output/newsletter_content.txt`: Text content of the newsletter
- `output/newsletter.html`: Final HTML newsletter ready for email




