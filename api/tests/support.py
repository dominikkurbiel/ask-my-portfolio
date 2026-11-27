"""Small helpers shared by tests."""

import math

from app.modules.embeddings import Vector


def cosine(a: Vector, b: Vector) -> float:
    """Cosine similarity: 1 = same direction (same meaning), 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
