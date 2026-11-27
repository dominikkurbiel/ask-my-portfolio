import asyncio
from collections.abc import Iterable, Sequence
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding
from numpy.typing import NDArray

from app.modules.embeddings.port import Vector


class FastEmbedEmbedder:
    """Local embedding model run with fastembed (ONNX on CPU): no API key, no per-call cost.

    The model (hundreds of MB) is downloaded and loaded on first use, not at import time.
    Embedding is CPU-bound and blocking, so it runs in a worker thread: the event loop keeps
    serving other requests meanwhile.
    """

    def __init__(self, model_name: str, cache_dir: Path | None = None) -> None:
        self._model_name = model_name
        self._dimensions = _supported_dimensions(model_name)
        self._cache_dir = cache_dir
        self._model: TextEmbedding | None = None
        self._lock = asyncio.Lock()

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        if not texts:
            return []
        model = await self._loaded_model()
        return await asyncio.to_thread(lambda: _to_vectors(model.passage_embed(list(texts))))

    async def embed_query(self, text: str) -> Vector:
        model = await self._loaded_model()
        vectors = await asyncio.to_thread(lambda: _to_vectors(model.query_embed(text)))
        return vectors[0]

    async def _loaded_model(self) -> TextEmbedding:
        # The lock makes concurrent first calls load the model once, not several times
        async with self._lock:
            if self._model is None:
                cache_dir = str(self._cache_dir) if self._cache_dir else None
                self._model = await asyncio.to_thread(
                    TextEmbedding, model_name=self._model_name, cache_dir=cache_dir
                )
            return self._model


def _supported_dimensions(model_name: str) -> int:
    for model in TextEmbedding.list_supported_models():
        if model["model"] == model_name:
            return int(model["dim"])
    raise ValueError(f"fastembed does not support the embedding model {model_name!r}")


def _to_vectors(arrays: Iterable[NDArray[np.generic]]) -> list[Vector]:
    return [[float(x) for x in array.astype(np.float64)] for array in arrays]
