import requests

my_sentiment = "I am very happy with the service."
response = requests.post("http://localhost:8000/", json=my_sentiment)
print(response.json())
