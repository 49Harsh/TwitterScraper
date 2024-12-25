
# README.md
# Twitter Trend Scraper

A Python application that scrapes Twitter trending topics using Selenium with proxy rotation, stores data in MongoDB, and provides a web interface for viewing results.

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   TWITTER_EMAIL=your_email@example.com
   TWITTER_PASSWORD=your_password
   PROXYMESH_AUTH=your_proxymesh_auth
   MONGODB_URI=mongodb://localhost:27017/
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Project Structure

- `src/`: Core application code
- `static/`: Static assets
- `templates/`: HTML templates
- `tests/`: Test files
- `config/`: Configuration files
- `logs/`: Application logs

## License

MIT License