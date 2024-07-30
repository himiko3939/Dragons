import random
import time
import requests

headers = {
    'Content-Type': 'application/json',
    'Referer': 'https://bot.dragonz.land/',
}

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File 'query_id.txt' tidak ditemukan.")
        return []
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat query_id: {e}")
        return []

def get_user_agent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragents = [line.strip() for line in f.readlines()]
        if index < len(useragents):
            return useragents[index]
        else:
            return "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat user agent: {e}")
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

def get_me(query):
    url = 'https://bot.dragonz.land/api/me'
    headers['X-Init-Data'] = query

    try:
        response = requests.get(url, headers=headers)
        if 200 <= response.status_code < 300:
            return response.json()
        elif 500 <= response.status_code < 530:
            print(f"Server error: {response.text}")
        elif 400 <= response.status_code < 410:
            print(f"Client error: {response.status_code}")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    return None

def feed(query, feed_count):
    url = 'https://bot.dragonz.land/api/me/feed'
    headers['X-Init-Data'] = query
    payload = {'feedCount': feed_count}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if 200 <= response.status_code < 300:
            return "DONE"
        elif 500 <= response.status_code < 530:
            print(f"Server error: {response.text}")
        elif 400 <= response.status_code < 410:
            print(f"Client error: {response.status_code}")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    return None

def main():
    while True:
        queries = load_credentials()
        for index, query in enumerate(queries):
            user_agent = get_user_agent(index)
            headers['User-Agent'] = user_agent
            print(f"========= Account {index + 1} =========")
            data_getme = get_me(query)
            if data_getme:
                first_name = data_getme.get('firstName', 'Unknown')
                last_name = data_getme.get('lastName', 'Unknown')
                energy = data_getme.get('energy', 0)
                print(f"Name: {first_name} {last_name} | Energy: {energy}")
                while energy > 10:
                    time.sleep(2)  # Wait for 2 seconds before sending feed
                    feeds = random.randint(100, 200)
                    if energy < feeds:
                        feeds = energy
                    if feed(query, feeds):
                        print(f"Feeds {feeds} Clicks")
                        energy -= feeds
                    if energy <= 10:
                        break
            else:
                print("Error getting data")
            time.sleep(1)  # Wait for 1 second before moving to the next account

if __name__ == "__main__":
    main()
