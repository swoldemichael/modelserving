import requests

sentiment_text = {"sentiment_text":"I am very happy with the service."}

response = requests.get(url="http://localhost:8000/", params=sentiment_text)
print(response.json())
