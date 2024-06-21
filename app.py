from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def extract_currency_pairs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://qxbroker.com/en/demo-trade"

        while True:
            page.goto(url)
            page.wait_for_load_state('load')
            if page.url == url:
                break
        
        page.click('use[xlink:href="/profile/images/spritemap.svg#icon-plus"]')
        page.wait_for_selector('div.assets-table')

        currency_pairs = []
        assets_table = page.query_selector('div.assets-table')
        divs = assets_table.query_selector_all('div.assets-table__header div')
        
        for div in divs:
            currency_pairs.append(div.inner_text())
        
        browser.close()
        
        return currency_pairs

@app.route('/currency-pairs', methods=['GET'])
def get_currency_pairs():
    currency_pairs = extract_currency_pairs()
    return jsonify(currency_pairs)

if __name__ == '__main__':
    app.run(debug=True)
