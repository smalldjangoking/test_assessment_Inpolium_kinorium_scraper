# 🎬 Kinorium Scraper

A robust data collection system for scraping content from [ua.kinorium.com](https://ua.kinorium.com). Built with modern Python tools including FastAPI, Playwright, Pydantic, beautifulsoup4 and aiohttp.

## ⚠️ Important Notes

Before you start, please read this carefully:

- **Ukrainian IP Required**: For reliable operation and to avoid access restrictions, use a clean Ukrainian IP address.
- **HTTP Headers**: The site has anti-scraping measures in place. Default headers are included, but they may expire. Don't worry—if that happens, instructions below will show you how to get fresh ones.

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/smalldjangoking/test_assessment_Inpolium_kinorium_scraper.git
   cd test_assessment_Inpolium_kinorium_scraper
```

2. **Set up virtual environment**
```bash
   python -m venv venv
```

3. **Activate the environment**
   
   Windows:
```bash
   .\venv\Scripts\activate
```
   
   macOS/Linux:
```bash
   source venv/bin/activate
```

4. **Upgrade pip and install dependencies**
```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
```

### Configuration (Optional but Recommended)

If Method 1 (HTTP scraper) stops working, you'll need to update the authentication headers:

1. Create a `.env` file in the project root
2. Navigate to [ua.kinorium.com/R2D2/](https://ua.kinorium.com/R2D2/)
3. Open browser DevTools (F12)
4. Go to the Network tab
5. Find the request to `https://ua.kinorium.com/handlers/filmList/`
6. Extract the following values and add them to your `.env` file:
```env
SESSION="your_session_value"
X119="your_x119_value"
PHPSESSID="your_phpsessid_value"
USER_AGENT="your_browser_user_agent"
```

### Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app
```

Once running, open your browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:8000/docs`) to access the API documentation.

## 🛠 Tech Stack

- **FastAPI** - framework for building APIs
- **Playwright** - Browser automation for dynamic content
- **Pydantic** - Data validation and serialization
- **aiohttp** - Asynchronous HTTP client
- **beautifulsoup4** - HTML parsing and extraction
---

**Note**: Please use this scraper responsibly and in accordance with the website's terms of service.
