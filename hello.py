import adapters

import requests
from starlette.requests import Request
from typing import Dict

from ray import serve

# 1: Define a Ray Serve application.
@serve.deployment
class HelloWorld:
    def __init__(self, msg: str):
        # Initialize model state: could be very large neural net weights.
        self._msg = msg

    def __call__(self, request: Request) -> Dict:
        return {"result": f"{self._msg} = adapters vesion is {adapters.__version__}"}


app = HelloWorld.bind(msg="Hello world!")
