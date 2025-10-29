"""
Inference pipeline: choose model source + generation logic
"""
from .model import ModelLoader

class InferencePipeline:
    def __init__(self, loader: ModelLoader):
        self.loader = loader

    def generate(self, prompt):
        result = self.loader.generate_ollama(prompt)
        if not result:
            result = self.loader.generate_hf(prompt)
        return result
