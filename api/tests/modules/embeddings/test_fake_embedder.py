import math

import pytest

from app.modules.embeddings import FakeEmbedder
from tests.support import cosine


@pytest.fixture
def embedder() -> FakeEmbedder:
    return FakeEmbedder(dimensions=32)


async def test_returns_one_normalized_vector_per_text(embedder: FakeEmbedder) -> None:
    vectors = await embedder.embed_documents(["first text", "second text"])

    assert len(vectors) == 2
    for vector in vectors:
        assert len(vector) == 32
        assert math.isclose(math.sqrt(sum(x * x for x in vector)), 1.0)


async def test_same_text_gives_same_vector(embedder: FakeEmbedder) -> None:
    query = await embedder.embed_query("Real-time sync with WebSockets")
    document = (await embedder.embed_documents(["Real-time sync with WebSockets"]))[0]

    assert query == document


async def test_texts_sharing_words_are_more_similar(embedder: FakeEmbedder) -> None:
    query = await embedder.embed_query("websockets real-time")
    related, unrelated = await embedder.embed_documents(
        ["Built real-time collaboration with WebSockets and Yjs", "Pierogi recipe with cheese"]
    )

    assert cosine(query, related) > cosine(query, unrelated)


async def test_handles_polish_characters_and_case(embedder: FakeEmbedder) -> None:
    lower = await embedder.embed_query("zażółć gęślą jaźń")
    upper = await embedder.embed_query("ZAŻÓŁĆ GĘŚLĄ JAŹŃ")

    assert lower == upper


async def test_empty_input(embedder: FakeEmbedder) -> None:
    assert await embedder.embed_documents([]) == []
    assert await embedder.embed_query("") == [0.0] * 32
