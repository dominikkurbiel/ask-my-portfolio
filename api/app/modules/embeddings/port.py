from collections.abc import Sequence
from typing import Protocol

type Vector = list[float]


class Embedder(Protocol):
    """Turns text into vectors that capture its meaning (similar meaning -> nearby vectors).

    Documents and queries have separate methods because some models embed them differently
    (e.g. with "passage:" / "query:" prefixes). Callers never need to know which model is used.
    """

    @property
    def model_name(self) -> str:
        """Stored next to every vector: vectors from different models are not comparable."""
        ...

    @property
    def dimensions(self) -> int:
        """Length of every vector this embedder returns."""
        ...

    async def embed_documents(self, texts: Sequence[str]) -> list[Vector]:
        """One vector per text, in the same order."""
        ...

    async def embed_query(self, text: str) -> Vector: ...
