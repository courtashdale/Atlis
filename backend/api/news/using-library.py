from newsapi import NewsApiClient

# Initialize client
newsapi = NewsApiClient(api_key='25700442d2c24e159b0507ff6c67c1ab')

# Get top headlines
top_headlines = newsapi.get_top_headlines(
    q='bitcoin',
    country='us',
    category='business',
    language='en'
)

# Get all articles
all_articles = newsapi.get_everything(
    q='bitcoin',
    from_param='2025-06-20',
    to='2025-06-25',
    language='en',
    sort_by='relevancy',
    page_size=50,
    page=1
)

# Get all sources
sources = newsapi.get_sources()

# Print articles
for article in all_articles['articles']:
    print("🔹", article['title']['description'])