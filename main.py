import requests
from twilio.rest import Client
STOCK_NAME = "TWTR"
COMPANY_NAME = "Twitter Inc"

# API Endpoints
# Stock Endpoint and api details
STOCK_ENDPOINT = ""
STOCK_ENDPOINT_1= ""

STOCK_API_KEY = ""
stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

# News Endpoint and api details
NEWS_ENDPOINT = ""
NEWS_API_KEY = ""

news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME # use q in title and a different stock
}

# Twillo API for texting the user
TWILLO_ACC_SID = ""
TWILLO_AUTH_TOKEN = ""

# Prices of stocks from Stocks api
response_stock = requests.get(url=STOCK_ENDPOINT, params=stock_param)
response_stock.raise_for_status()

response_stock_dict = response_stock.json()['Time Series (Daily)']

# All closing prices
closing_prices = [float(value['4. close']) for (key, value) in response_stock_dict.items()]

# Closing price for yesterday

yesterday_closing_price = closing_prices[0]

# Closing price for day before yesterday

day_before_yesterday_closing_price = closing_prices[1]
print(yesterday_closing_price, day_before_yesterday_closing_price)

# Difference between the closing prices

difference = yesterday_closing_price - day_before_yesterday_closing_price
print("{:.2f}".format(difference))

# To check if closing price rose by 5% or not
diff_percentage = (difference / yesterday_closing_price) * 100
print(diff_percentage)
# To get news of the following stock
if abs(diff_percentage) > 0.2:
    response_news = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    response_news.raise_for_status()
    articles = response_news.json()['articles']
    three_articles = articles[:3]
    formatted_articles = [f"Headline: {article['title']} \n\nBrief: {article['description']}" for article in three_articles]
    article_titles = [three_articles[i]['title'] for i in range(0, 3)]
    article_descriptions = [three_articles[_]['description']for _ in range(0, 3)]
    client = Client(TWILLO_ACC_SID, TWILLO_AUTH_TOKEN)
    if difference > 0:
        emoji = "🔺"
    else:
        emoji = "🔻"

    for msgs in range(0, 3):
        message = client.messages \
            .create(
            body=f"{STOCK_NAME}: {emoji}{difference:.2f}\n\n{formatted_articles[msgs]}",
            from_='',# Sender's phone number
            to=''# Receiver's phone number
        )
        print(message.status)





"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

