"""Text embeddings behind a small port, so the rest of the app never depends on a model."""

from app.config import Settings
from app.modules.embeddings.fake import FakeEmbedder
from app.modules.embeddings.fastembed_embedder import FastEmbedEmbedder
from app.modules.embeddings.port import Embedder, Vector


def create_embedder(settings: Settings) -> Embedder:
    """The embedder the app uses, chosen by configuration."""
    return FastEmbedEmbedder(settings.embedding_model, settings.embedding_cache_dir)


__all__ = ["Embedder", "FakeEmbedder", "FastEmbedEmbedder", "Vector", "create_embedder"]
