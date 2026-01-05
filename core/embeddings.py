from functools import lru_cache
from typing import List
import asyncio
import aiohttp
import numpy as np
import llama_index.core.embeddings as BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings

class CachedHuggingFaceEmbeddings(HuggingFaceInferenceAPIEmbeddings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Cache up to 1000 embeddings
        self._cached_embed = lru_cache(maxsize=1000)(self._embed_uncached)

    def _embed_uncached(self, text: str) -> List[float]:
        """Internal method without caching"""
        return super().get_text_embedding(text)

    async def _aembed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Process embeddings in batches with async"""
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            # Process batch asynchronously
            batch_results = await asyncio.gather(*[
                self._aget_text_embedding(text) for text in batch
            ])
            results.extend(batch_results)
        return results

    def get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text with caching"""
        return self._cached_embed(text)

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts with batching"""
        # Run async batch processing
        return asyncio.run(self._aembed_batch(texts))
