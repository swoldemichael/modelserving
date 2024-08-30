import requests
from starlette.requests import Request

from ray import serve

# 1: Define a Ray Serve application.
@serve.deployment()
class HelloWorld:
    def __init__(self, msg: str):
        # Initialize model state: could be very large neural net weights.
        self._msg = msg
       

    def __call__(self, request: Request) -> dict:
        import adapters
        import torch
        import transformers
        return {"result": f"{self._msg} versions are is {torch.__version__}, {transformers.__version__}, {adapters.__version__}"}


app = HelloWorld.options( ray_actor_options={"runtime_env": {"pip": ["torch==2.4.0+cu121","transformers==4.43.3","adapters==1.0.0"]}}).bind(msg="Hello world!")
