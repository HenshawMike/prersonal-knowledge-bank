from functools import lru_cache
from typing import List, Optional, Dict, Any
from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbedding
from llama_index.core.embeddings import BaseEmbedding

class CachedHuggingFaceEmbeddings(BaseEmbedding):
    """Cached HuggingFace Inference API embeddings with synchronous interface."""
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L12-v2",
        api_key: Optional[str] = None,
        api_base: str = "https://router.huggingface.co",
        **kwargs
    ):
        """
        Initialize with HuggingFace Inference API settings.
        
        Args:
            model_name: Name of the model to use
            api_key: HuggingFace API key
            api_base: Base URL for the API endpoint
            **kwargs: Additional arguments to pass to HuggingFaceInferenceAPIEmbedding
        """
        super().__init__(**kwargs)
        self._model_name = model_name
        self._api_key = api_key
        self._api_base = api_base
        self._embedder = HuggingFaceInferenceAPIEmbedding(
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            **kwargs
        )

    @lru_cache(maxsize=1000)
    def _get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text with caching."""
        return self._embedder._get_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        return [self._get_text_embedding(text) for text in texts]

    def get_text_embedding(self, text: str) -> List[float]:
        """Public method to get embedding for a single text."""
        return self._get_text_embedding(text)

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Public method to get embeddings for multiple texts."""
        return self._get_text_embeddings(texts)

    # Required by BaseEmbedding
    def _get_query_embedding(self, query: str) -> List[float]:
        return self.get_text_embedding(query)

    def _get_agg_embedding_from_queries(
        self, queries: List[str]
    ) -> List[float]:
        """Get aggregated embedding from multiple queries (average pooling)."""
        embeddings = self.get_text_embeddings(queries)
        if not embeddings:
            return []
        return [sum(x) / len(x) for x in zip(*embeddings)]