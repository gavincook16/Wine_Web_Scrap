import requests


def fetch_titles_and_prices(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()

        # Navigate through the JSON structure based on expected format
        items = data.get('data', {}).get('search', {}).get('products', [])
        products = []
        for item in items:
            title = item.get('item', {}).get('product_description', {}).get('title')
            price_info = item.get('price', {}).get('current_retail')
            products.append((title, price_info))

        return products
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


if __name__ == "__main__":
    search_term = "austin+hope"
    storeId = 2759
    url = f"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_dmc_dmr=true&include_sponsored=true&keyword={search_term}&new_search=true&offset=0&page=%2Fs%2Ftest&platform=desktop&pricing_store_id={storeId}&scheduled_delivery_store_id={storeId}&store_ids={storeId}%2C1120%2C309%2C2872%2C3298&useragent=Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_15_7%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F124.0.0.0+Safari%2F537.36&visitor_id=018F37554DC402019DD693CAFD4B21FF&zip=93401"
    products = fetch_titles_and_prices(url)
    if products:
        for title, price in products:
            print(f"Title: {title}, Price: {price}")
    else:
        print("No products found or there was an error.")