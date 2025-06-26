import os
import requests
from dotenv import find_dotenv, load_dotenv
from datetime import date

# Getting News API Key
_ = load_dotenv(find_dotenv())
key = os.getenv("NEWS_API_KEY")
print(f'API Key={key}')

# Setting today's date
today = str(date.today())
print(f'Todays date={today}')

base_url = "https://newsapi.org/v2/everything"
query = "Israel and Iran"
start_date = "2025-06-01"
end_date = today
sort_option = "popularity"
'''
	•	relevancy – Best when the search term is general or ambiguous. Prioritizes textual relevance.
	•	popularity – Best for trending topics where big outlets matter (e.g., political headlines).
	•	publishedAt – Best when you want a real-time feed or timeline of events.
'''

url = f"{base_url}?q={query}&from={start_date}&to={start_date}&sortBy={sort_option}&apiKey={key}"

basic_url = ('https://newsapi.org/v2/everything?q=Trump&from=2025-06-26&sortBy=popularity&apiKey=25700442d2c24e159b0507ff6c67c1ab')

response = requests.get(url)

print(response.status_code)
print(response.json())