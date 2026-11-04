# Aura Sathi - AI Shopping Bodyguard

A Streamlit-based AI application that scans product labels and evaluates them against your personalized health profile using Google Gemini AI.

## Features

- **AI Product Scanner** - Upload or capture product label images for instant analysis
- **Digital Twin Health Profile** - Personalized allergen & dietary restriction monitoring
- **WHO Guideline Compliance** - Cross-references ingredients against World Health Organization standards
- **Live Price Comparison** - Compares prices across Indian e-commerce platforms (Blinkit, Amazon, Zepto, Instamart)
- **Voice Verdicts** - AI-generated audio summaries of product safety
- **Scan History & Analytics** - Dashboard with metrics, charts, and exportable audit reports
- **User Authentication** - Secure email/password registration and login
- **Persistent Storage** - SQLite database with SQLAlchemy ORM

## Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone the repository
cd AuraSathi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run the app
streamlit run app.py
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key for AI analysis |
| `DATABASE_URL` | No | Database connection string (default: sqlite:///aura_sathi.db) |

## Project Structure

```
AuraSathi/
├── app.py                 # Main entry point
├── config/                # Configuration settings
│   ├── __init__.py
│   └── settings.py
├── models/                # Pydantic models & SQLAlchemy DB models
│   ├── __init__.py
│   ├── user.py            # UserProfile model with validation
│   ├── product.py         # ProductAnalysis & PriceItem
│   ├── scan_record.py     # ScanRecord model
│   └── database.py        # SQLAlchemy ORM models
├── services/              # Business logic
│   ├── __init__.py
│   ├── ai_service.py      # Gemini AI integration
│   ├── audio_service.py   # gTTS voice generation
│   ├── history_service.py # Scan history & metrics
│   ├── database_service.py# Database operations
│   ├── auth_service.py    # User authentication
│   └── export_service.py  # CSV audit export
├── ui/                    # Streamlit UI components
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page views
│   └── styles.py          # Custom CSS theme
├── utils/                 # Utilities
│   ├── session.py         # Session state management
│   ├── logging_config.py  # Logging setup
│   ├── validation.py      # Input validation & sanitization
│   └── types.py           # Type hints & TypedDict
├── tests/                 # Pytest test suite
└── requirements.txt
```

## Usage

1. **Register/Login** - Create an account or sign in
2. **Setup Digital Twin** - Configure your health profile (allergies, dietary preferences, biometrics)
3. **Scan Products** - Use camera or upload product label images
4. **View Results** - See AI verdict (BUY/THINK/AVOID), safety score, WHO compliance, prices
5. **Track History** - Dashboard shows metrics, trends, and full scan history
6. **Export Audit** - Download comprehensive CSV health audit report

## API Integration

### Gemini AI Service
```python
from services.ai_service import analyze_product_image

analysis = analyze_product_image(
    image_bytes=img_bytes,
    mime_type="image/jpeg",
    user_data={"age": 28, "health": "Peanut allergy", "interests": ["Fitness"]}
)
```

### Database Operations
```python
from services.database_service import save_scan_record, get_scan_history

save_scan_record(record, analysis, user_id="user-uuid")
history = get_scan_history(user_id="user-uuid", limit=50)
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=services --cov=models --cov=utils
```

## Tech Stack

- **Frontend**: Streamlit 1.30+
- **AI**: Google Gemini 2.5 Flash (google-genai)
- **Database**: SQLite + SQLAlchemy 2.0
- **Charts**: Altair 5.0+
- **Voice**: gTTS (Google Text-to-Speech)
- **Validation**: Pydantic 2.0 + bleach
- **Auth**: bcrypt password hashing
- **Testing**: pytest + pytest-mock

## Security

- Passwords hashed with bcrypt
- Input sanitization with bleach (XSS prevention)
- Email format validation
- Password strength requirements
- File upload validation (type & size)
- SQL injection prevention via SQLAlchemy ORM

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest`
5. Submit a pull request

## Support

For issues and feature requests, please open a GitHub issue.