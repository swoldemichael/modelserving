from transformers import AutoTokenizer, TextClassificationPipeline
from adapters import AutoAdapterModel

from starlette.requests import Request
from ray import serve

@serve.deployment
class SentimentClassifier:
  def __init__(self):
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    model = AutoAdapterModel.from_pretrained("roberta-base")
    adapter_name = model.load_adapter("solwol/my-awesome-adapter", source="hf", set_active=True)
    self.model = TextClassificationPipeline(model=model, tokenizer=tokenizer)

  def classify(self, sentiment: str) -> dict:
    output = self.model(sentiment)
    return output[0]

  async def __call__(self, http_request: Request) -> dict:
    sentiment_text = await http_request.json()
    return self.classify(sentiment_text)

sentiment_app = SentimentClassifier.bind()
