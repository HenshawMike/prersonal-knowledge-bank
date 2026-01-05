from functools import lru_cache
from typing import List
from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbedding

class CachedHuggingFaceEmbeddings(HuggingFaceInferenceAPIEmbedding):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Wrap the sync get_text_embedding method with LRU caching
        self._cached_embed = lru_cache(maxsize=1000)(self.get_text_embedding)

    def get_text_embedding(self, text: str) -> List[float]:
        """Return embedding for a single text (cached)"""
        return self._cached_embed.__wrapped__(self, text)  # call original method

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for multiple texts"""
        # Just call get_text_embedding repeatedly; no asyncio
        return [self.get_text_embedding(t) for t in texts]
