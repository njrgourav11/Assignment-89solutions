# News Summarizer Script

A robust Python application to fetch and summarize news articles using the NewsAPI. This project improves upon an initial script by adding security, error handling, filtering capabilities, and a modern Web UI.

## 🚀 Getting Started

### Prerequisites

-   **Python 3.x**: Ensure Python is installed on your system.
-   **NewsAPI Key**: You need a free API key from [NewsAPI.org](https://newsapi.org/register).

### Installation

1.  **Clone/Download** the repository to your local machine.
2.  **Install Dependencies**: Open your terminal (Command Prompt or PowerShell) in the project folder and run:
    ```bash
    python -m pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    -   Create a new file named `.env` in the same folder.
    -   Add your API key to it like this:
        ```env
        NEWS_API_KEY=your_actual_api_key_from_website
        ```
    -   *Note: A `.env.example` file is provided for reference.*

---

## 🖥 Web UI Usage (Recommended)

The easiest way to use the application is through the modern Web Interface.

1.  **Start the Server**:
    ```bash
    python app.py
    ```
2.  **Open in Browser**:
    Go to [http://127.0.0.1:5000](http://127.0.0.1:5000).
3.  **Use**: Enter keywords or select dates to filter news visually.

---

## 💻 CLI Usage (Command Line)

You can also run the script directly from your terminal.

### 1. Basic Usage (Top Headlines)
Fetches top headlines from BBC News.
```bash
python news_summarizer_buggy.py
```

### 2. Filter by Keyword
Search for specific topics (e.g., "Technology").
```bash
python news_summarizer_buggy.py --keyword "Technology"
```

### 3. Filter by Date Range
Get news from a specific timeframe (YYYY-MM-DD).
```bash
python news_summarizer_buggy.py --from 2024-01-01 --to 2024-01-07
```

### 4. Combine Filters
```bash
python news_summarizer_buggy.py --keyword "Crypto" --from 2024-01-01
```

### 5. Help
View all available options.
```bash
python news_summarizer_buggy.py --help
```

---

## 🔧 Technical Report: Issues & Fixes

Below is a detailed breakdown of the original issues and the complete implementation details.

### 1. Broken API Endpoint (Functional Issue)
-   **Issue**: The original script used the deprecated v1 API (`https://newsapi.org/v1/articles`), which caused immediate crashes.
-   **Fix**: Migrated to v2 endpoints (`v2/top-headlines` for general news and `v2/everything` for detailed searching).

### 2. Hardcoded API Key (Security Vulnerability)
-   **Issue**: The API key was hardcoded in the script, posing a security risk if shared.
-   **Fix**: Implemented `python-dotenv`. The key is now stored in a `.env` file (excluded from git via `.gitignore`) and loaded into environment variables at runtime.

### 3. Lack of Error Handling (Robustness)
-   **Issue**: Any network or API failure would crash the script.
-   **Fix**: Added robust `try-except` blocks to handle:
    -   Network connectivity issues.
    -   HTTP errors (404, 500) using `response.raise_for_status()`.
    -   API-specific error messages (e.g., "Invalid Key").

### 4. Missing Features (Enhancement)
-   **Issue**: No way to filter news.
-   **Fix**: Integrated `argparse` to accept command-line arguments for keywords and date ranges.

### 5. Web UI Implementation (New Feature)
-   **Architecture**:
    -   **Backend (Flask)**: A lightweight Python web server (`app.py`) accepts requests from the browser, securely adds the API key, and forwards the request to NewsAPI. This prevents exposing the API key to the client and solves CORS (Cross-Origin Resource Sharing) issues.
    -   **Frontend (HTML/CSS/JS)**: A responsive interface (`templates/index.html`) that fetches data from our local Flask server and renders news cards dynamically with images and descriptions.

---

## ☁️ Deployment (Vercel)

This project is configured for deployment on Vercel.

1.  **Configuration**: A `vercel.json` file is included to tell Vercel to use the Python runtime for `app.py`.
2.  **Steps**:
    -   Push code to GitHub.
    -   Import project in Vercel.
    -   **Important**: Add `NEWS_API_KEY` in Vercel's Environment Variables settings.
