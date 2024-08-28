from transformers import AutoTokenizer, TextClassificationPipeline
from adapters import AutoAdapterModel

from fastapi import FastAPI
from ray import serve

app = FastAPI()

@serve.deployment
@serve.ingress(app)
class SentimentClassifier:
  def __init__(self):
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    model = AutoAdapterModel.from_pretrained("roberta-base")
    adapter_name = model.load_adapter("solwol/my-awesome-adapter", source="hf", set_active=True)
    self.model = TextClassificationPipeline(model=model, tokenizer=tokenizer)

  def classify(self, sentiment: str) -> dict:
    output = self.model(sentiment)
    return output[0]
  
  @app.get("/")
  async def call_classifier(self, sentiment_text: str) -> dict:
    return self.classify(sentiment_text)

sentiment_app = SentimentClassifier.bind()
