"""Runs the real local model. Excluded by default (downloads ~1 GB): uv run poe test-model"""

import pytest

from app.config import get_settings
from app.modules.embeddings import FastEmbedEmbedder
from tests.support import cosine

pytestmark = pytest.mark.model


@pytest.fixture(scope="module")
def embedder() -> FastEmbedEmbedder:
    settings = get_settings()
    return FastEmbedEmbedder(settings.embedding_model, settings.embedding_cache_dir)


async def test_vectors_have_the_model_dimensions(embedder: FastEmbedEmbedder) -> None:
    vectors = await embedder.embed_documents(["one", "two"])

    assert [len(v) for v in vectors] == [embedder.dimensions] * 2


async def test_polish_question_finds_english_text_by_meaning(embedder: FastEmbedEmbedder) -> None:
    # No shared words: only a multilingual model that understands meaning can match these
    query = await embedder.embed_query("Czy pracował z komunikacją w czasie rzeczywistym?")
    related, unrelated = await embedder.embed_documents(
        [
            "Built live collaboration over WebSockets: cursors and edits sync between users.",
            "Enjoys hiking in the mountains and baking bread on weekends.",
        ]
    )

    assert cosine(query, related) > cosine(query, unrelated)


async def test_unknown_model_is_rejected() -> None:
    with pytest.raises(ValueError, match="does not support"):
        FastEmbedEmbedder("no-such/model")
