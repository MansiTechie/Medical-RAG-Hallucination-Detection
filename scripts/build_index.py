"""
Ingestion script: PDF → FAISS index + metadata.json

Replicates the exact chunking and embedding logic from Notebook 03/08:
  - PDF text extraction with PyMuPDF
  - Text cleaning (collapse whitespace)
  - RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  - all-MiniLM-L6-v2 embeddings (dim=384)
  - FAISS IndexFlatL2
  - metadata.json with chunk_id, page, text per chunk

Output:
  vector_db/index.faiss
  vector_db/metadata.json
"""

import os
import re
import sys
import json
import numpy as np

# Ensure project root is importable
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)

# ── Configuration (matches Notebook 08) ──────────────────────────
PDF_PATH = os.path.join(
    PROJECT_ROOT, "dataset", "raw",
    "niddk_guiding_principles_diabetes.pdf"
)
VECTOR_DB_DIR = os.path.join(PROJECT_ROOT, "vector_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def main():
    # ── 1. Validate PDF ──────────────────────────────────────────
    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    print(f"PDF path: {PDF_PATH}")

    # ── 2. Extract text ──────────────────────────────────────────
    import pymupdf  # fitz

    doc = pymupdf.open(PDF_PATH)
    print(f"Total pages: {len(doc)}")

    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            pages.append({"page": page_number, "text": text})

    doc.close()
    print(f"Pages with text: {len(pages)}")

    # ── 3. Chunk text ────────────────────────────────────────────
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for page_data in pages:
        page_chunks = text_splitter.split_text(page_data["text"])
        for chunk_id, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_id": f"page_{page_data['page']}_chunk_{chunk_id}",
                "page": page_data["page"],
                "text": chunk_text
            })

    print(f"Total chunks: {len(chunks)}")

    # ── 4. Generate embeddings ───────────────────────────────────
    from sentence_transformers import SentenceTransformer

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(
        texts, show_progress_bar=True
    ).astype("float32")

    print(f"Embedding shape: {embeddings.shape}")

    # ── 5. Build FAISS index ─────────────────────────────────────
    import faiss

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    print(f"FAISS vectors: {index.ntotal}")

    # ── 6. Save ──────────────────────────────────────────────────
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    index_path = os.path.join(VECTOR_DB_DIR, "index.faiss")
    metadata_path = os.path.join(VECTOR_DB_DIR, "metadata.json")

    faiss.write_index(index, index_path)
    print(f"Saved FAISS index: {index_path}")

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Saved metadata: {metadata_path}")

    print("\nIngestion complete.")
    print(f"  Chunks: {len(chunks)}")
    print(f"  Dimensions: {embeddings.shape[1]}")
    print(f"  Index: {index_path}")
    print(f"  Metadata: {metadata_path}")


if __name__ == "__main__":
    main()
