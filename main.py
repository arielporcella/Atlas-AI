from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_site(url, selector="a", base_url=None, limit=5):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        results = []
        for item in soup.select(selector)[:limit]:
            title = item.get_text(strip=True)
            href = item.get("href")
            if href:
                link = href if href.startswith("http") else (base_url or url) + href
            else:
                link = url
            results.append({"title": title, "link": link})
        return results
    except Exception as e:
        return [{"error": f"{str(e)} – site: {url}"}]

@app.route("/visas", methods=["GET"])
def get_all_sources():
    data = {
        "travel_state": scrape_site(
            "https://travel.state.gov/content/travel/en/us-visas.html",
            ".tsg-rwd-title-link a",
            "https://travel.state.gov"
        ),
        "uscis_home": scrape_site(
            "https://www.uscis.gov/",
            "a",
            "https://www.uscis.gov"
        ),
        "usa_gov": scrape_site(
            "https://www.usa.gov/immigration-and-citizenship",
            "a",
            "https://www.usa.gov"
        ),
        "cbp_home": scrape_site(
            "https://www.cbp.gov/",
            "a",
            "https://www.cbp.gov"
        ),
        "uscis_workers": scrape_site(
            "https://www.uscis.gov/working-in-the-united-states/temporary-nonimmigrant-workers",
            ".usa-accordion__button",
            "https://www.uscis.gov"
        )
    }
    return jsonify({"status": "success", "data": data})

@app.route("/", methods=["GET"])
def index():
    return "Atlas IA – API de pesquisa de vistos e imigração (v1.3)"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

