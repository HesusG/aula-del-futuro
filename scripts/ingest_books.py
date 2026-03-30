"""Ingest PDFs from libros/ into a local ChromaDB vector database."""
import io
import os
import sys
import fitz
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
    # Use local tessdata if available (for Spanish OCR)
    local_tessdata = os.path.join(os.path.expanduser("~"), "tessdata")
    if os.path.isdir(local_tessdata):
        os.environ.setdefault("TESSDATA_PREFIX", local_tessdata)
except ImportError:
    HAS_OCR = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBROS_DIR = os.path.join(ROOT, "libros")
CHROMA_DIR = os.path.join(ROOT, "chromadb_data")

BOOK_MAP = {
    "Libro Enseñanza Situada.pdf": {
        "id": "diaz-barriga-2006",
        "title": "Enseñanza situada: Vínculo entre la escuela y la vida",
        "author": "Díaz Barriga Arceo, F.",
    },
    "6 Facetas de la Comprensioìn (1).pdf": {
        "id": "wiggins-mctighe-2017-facetas",
        "title": "Las seis facetas de la comprensión",
        "author": "Wiggins, G. y McTighe, J.",
    },
    "Wiggins, G. y Mc Tighe, J. (2017) Planear para el aprendizaje. en Enseñar a través de la comprensión. México_ Trillas. Pág.153-178.pdf": {
        "id": "wiggins-mctighe-2017-planear",
        "title": "Planear para el aprendizaje",
        "author": "Wiggins, G. y McTighe, J.",
    },
    "estrategias de E-A-pimienta prieto.pdf": {
        "id": "pimienta-2012",
        "title": "Estrategias de enseñanza-aprendizaje",
        "author": "Pimienta Prieto, J. H.",
    },
    "librojuliopimientaestrategias.pdf": {
        "id": "pimienta-2007",
        "title": "Metodología constructivista: Guía para la planeación docente",
        "author": "Pimienta Prieto, J. H.",
    },
    "Presentacion de Socorro Guevara Estrategia de Enseñanza.pdf": {
        "id": "guevara-sf",
        "title": "Estrategia de Enseñanza",
        "author": "Guevara Salazar, M. S.",
    },
}

MAX_CHUNK = 2000
MIN_MERGE = 100


def chunk_page(text, page_num, book_meta):
    """Split page text into paragraph-based chunks with metadata."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) < MAX_CHUNK:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current)
            current = para

    if current and len(current) >= MIN_MERGE:
        chunks.append(current)
    elif current and chunks:
        chunks[-1] += f"\n\n{current}"
    elif current:
        chunks.append(current)

    results = []
    for i, chunk in enumerate(chunks):
        results.append({
            "id": f"{book_meta['id']}_p{page_num}_c{i}",
            "text": chunk,
            "metadata": {
                "book_id": book_meta["id"],
                "title": book_meta["title"],
                "author": book_meta["author"],
                "page": page_num,
                "chunk_index": i,
            },
        })
    return results


def ingest():
    print("Setting up embedding function (first run downloads the model)...")
    ef = SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    # Delete existing collection to re-ingest cleanly
    try:
        client.delete_collection("aula_libros")
    except Exception:
        pass
    collection = client.create_collection("aula_libros", embedding_function=ef)

    all_chunks = []
    for filename, meta in BOOK_MAP.items():
        path = os.path.join(LIBROS_DIR, filename)
        if not os.path.exists(path):
            print(f"  SKIP: {filename} not found")
            continue

        doc = fitz.open(path)
        num_pages = doc.page_count
        book_chunks = []
        ocr_used = False
        for page_num in range(num_pages):
            text = doc[page_num].get_text()
            # If no text found, try OCR on the page image
            if not text.strip() and HAS_OCR:
                images = doc[page_num].get_images()
                if images:
                    pix = doc[page_num].get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    ocr_lang = "spa" if os.path.exists(os.path.join(
                        os.environ.get("TESSDATA_PREFIX", ""), "spa.traineddata"
                    )) else "eng"
                    text = pytesseract.image_to_string(img, lang=ocr_lang)
                    ocr_used = True
            if not text.strip():
                continue
            page_chunks = chunk_page(text, page_num + 1, meta)
            book_chunks.extend(page_chunks)
        doc.close()

        suffix = " (OCR)" if ocr_used else ""
        print(f"  {meta['id']}: {len(book_chunks)} chunks from {num_pages} pages{suffix}")
        all_chunks.extend(book_chunks)

    if not all_chunks:
        print("ERROR: No chunks extracted. Check that libros/ contains the expected PDFs.")
        sys.exit(1)

    print(f"\nIngesting {len(all_chunks)} total chunks into ChromaDB...")

    # ChromaDB has a batch limit, insert in batches of 100
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        print(f"  Batch {i // batch_size + 1}/{(len(all_chunks) - 1) // batch_size + 1} done")

    print(f"\nDone! {collection.count()} chunks stored in {CHROMA_DIR}")


if __name__ == "__main__":
    ingest()
