import requests

payload = { 'api_key': 'cc31a553b05a7bea7b7b33bf013f9a1e', 'url': 'https://scholar.google.com/' }
r = requests.get('https://api.scraperapi.com/', params=payload)
print(r.text)
