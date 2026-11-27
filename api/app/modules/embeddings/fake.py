import hashlib
import math
import re
from collections.abc import Sequence

from app.modules.embeddings.port import Vector

_WORD = re.compile(r"\w+")


class FakeEmbedder:
    """Fast, deterministic embedder for tests: no model download, no network.

    A "hashing bag of words": every word adds 1 to one of `dimensions` buckets (picked by the
    word's hash), then the vector is normalized to length 1. Texts that share words get similar
    vectors, so search tests behave sensibly; it knows nothing about synonyms or other languages.
    """

    model_name = "fake-hashing-bag-of-words"

    def __init__(self, dimensions: int = 64) -> None:
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        return [self._embed(text) for text in texts]

    async def embed_query(self, text: str) -> Vector:
        return self._embed(text)

    def _embed(self, text: str) -> Vector:
        vector = [0.0] * self._dimensions
        for word in _WORD.findall(text.lower()):
            digest = hashlib.sha256(word.encode()).digest()
            vector[int.from_bytes(digest[:4], "big") % self._dimensions] += 1.0
        return _normalize(vector)


def _normalize(vector: Vector) -> Vector:
    length = math.sqrt(sum(x * x for x in vector))
    return vector if length == 0 else [x / length for x in vector]
