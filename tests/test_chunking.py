from app.services.chunking import chunk_text


def test_short_text_returns_single_chunk():
    chunks = chunk_text("Krátký text.")
    assert chunks == ["Krátký text."]


def test_long_text_splits_into_multiple_chunks():
    text = "".join(str(i % 10) for i in range(2500))
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    assert len(chunks) > 1
    assert all(len(c) <= 1000 for c in chunks)


def test_consecutive_chunks_overlap():
    text = "".join(str(i % 10) for i in range(2500))
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    # konec prvního chunku = začátek druhého (překryv 200 znaků)
    assert chunks[0][-200:] == chunks[1][:200]