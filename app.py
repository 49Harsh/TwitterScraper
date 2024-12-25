from flask import Flask, render_template
from twitter_scraper import TwitterScraper
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    scraper = TwitterScraper()
    try:
        trends = scraper.get_trending_topics()
        json_data = json.dumps(trends, default=str, indent=2)
        return f"""
        <html>
            <body>
                <h2>Latest Twitter Trends</h2>
                <p>These are the most happening topics as on {trends['timestamp']}:</p>
                <ul>
                    <li>{trends['nameoftrend1']}</li>
                    <li>{trends['nameoftrend2']}</li>
                    <li>{trends['nameoftrend3']}</li>
                    <li>{trends['nameoftrend4']}</li>
                    <li>{trends['nameoftrend5']}</li>
                </ul>
                <p>IP address: {trends['ip_address']}</p>
                <pre>{json_data}</pre>
                <form method="post">
                    <button type="submit">Refresh Trends</button>
                </form>
            </body>
        </html>
        """
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)