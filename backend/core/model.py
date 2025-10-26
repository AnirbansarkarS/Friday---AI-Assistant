from huggingface_hub import InferenceClient
from ..config import HF_API_KEY, INFERENCE_MODEL

_client = None

def get_inference_client():
global _client
if _client is None:
if not HF_API_KEY:
raise RuntimeError("HF_API_KEY is not set in env")
_client = InferenceClient(api_key=HF_API_KEY)
return _client

def generate_text(prompt: str, max_length: int = 256, model: str = None):
client = get_inference_client()
model_to_use = model or INFERENCE_MODEL
# Use the InferenceClient text generation when available
res = client.text_generation(model=model_to_use, inputs=prompt, parameters={"max_new_tokens": max_length})
# InferenceClient returns a list-like generator; we'll return text merged
if isinstance(res, (list, tuple)):
return "".join([r.get('generated_text', '') if isinstance(r, dict) else str(r) for r in res])
return str(res)