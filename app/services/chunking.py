def chunk_text(text: str, *, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size]
        if chunk:
            chunks.append(chunk)
    return chunks