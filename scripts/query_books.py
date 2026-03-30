"""Query the ChromaDB vector database of textbooks.

Usage:
  python scripts/query_books.py "aprendizaje situado"       # interactive query
  python scripts/query_books.py --reflect                    # predefined reflect queries
"""
import argparse
import json
import os
import sys

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(ROOT, "chromadb_data")
OUTPUT_PATH = os.path.join(ROOT, "scripts", "reflect_output.json")

REFLECT_QUERIES = {
    # 6 zonas
    "zona_investigar": "zona investigar indagación búsqueda de información pensamiento científico",
    "zona_crear": "zona crear diseñar construir prototipos creatividad producción",
    "zona_intercambiar": "zona intercambiar diálogo debate discusión colaboración entre pares",
    "zona_desarrollar": "zona desarrollar trabajo autónomo práctica individual metacognición",
    "zona_presentar": "zona presentar comunicar hallazgos exposición oral audiencia",
    "zona_interactuar": "zona interactuar tecnología herramientas digitales recursos multimedia",
    # Estrategias primaria
    "unidades_tematicas": "unidades temáticas integradas problemas reales proyectos interdisciplinarios primaria",
    "centros_aprendizaje": "centros de aprendizaje lúdico estaciones rotativas juego educativo manipulativos",
    "diarios_aprendizaje": "diarios de aprendizaje metacognición reflexión autorregulación escritura reflexiva",
    # Estrategias preparatoria
    "proyectos_capstone": "proyectos capstone alianzas comunitarias aprendizaje servicio vinculación",
    "rutas_personalizadas": "rutas de aprendizaje personalizadas autonomía diferenciación ritmo propio",
    "seminarios_socraticos": "seminarios socráticos debate estructurado pensamiento crítico diálogo",
    # Temas transversales
    "motivacion_intrinseca": "motivación intrínseca autodeterminación autonomía competencia relación",
    "diseno_universal": "diseño universal para el aprendizaje DUA múltiples medios representación",
    "evaluacion_formativa": "evaluación formativa retroalimentación continua proceso no solo resultado",
    "mobiliario_flexible": "mobiliario reconfigurable espacio flexible aula modular zonas diferenciadas",
    "socioemocional": "desarrollo socioemocional bienestar emociones clima escolar convivencia",
    "rol_docente": "rol docente mediador facilitador guía andamiaje acompañamiento",
}


def get_collection():
    ef = SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection("aula_libros", embedding_function=ef)


def query(collection, text, n_results=5):
    results = collection.query(query_texts=[text], n_results=n_results)
    entries = []
    for i in range(len(results["ids"][0])):
        entries.append({
            "id": results["ids"][0][i],
            "book_id": results["metadatas"][0][i]["book_id"],
            "title": results["metadatas"][0][i]["title"],
            "author": results["metadatas"][0][i]["author"],
            "page": results["metadatas"][0][i]["page"],
            "distance": round(results["distances"][0][i], 4),
            "text": results["documents"][0][i][:500],
        })
    return entries


def interactive(query_text):
    collection = get_collection()
    results = query(collection, query_text)
    print(f"\nTop {len(results)} results for: \"{query_text}\"\n")
    for i, r in enumerate(results, 1):
        print(f"--- {i}. {r['author']} - {r['title']} (p. {r['page']}) [dist: {r['distance']}] ---")
        print(r["text"])
        print()


def reflect():
    collection = get_collection()
    output = {}
    print(f"Running {len(REFLECT_QUERIES)} reflect queries...\n")
    for key, q in REFLECT_QUERIES.items():
        results = query(collection, q, n_results=3)
        output[key] = {"query": q, "results": results}
        top = results[0] if results else None
        if top:
            print(f"  {key}: {top['author']} p.{top['page']} (dist: {top['distance']})")
        else:
            print(f"  {key}: no results")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nReflect output saved to {OUTPUT_PATH}")


def main():
    parser = argparse.ArgumentParser(description="Query textbook vector database")
    parser.add_argument("query", nargs="?", help="Search query text")
    parser.add_argument("--reflect", action="store_true", help="Run predefined reflect queries")
    args = parser.parse_args()

    if not os.path.exists(CHROMA_DIR):
        print("ERROR: chromadb_data/ not found. Run ingest_books.py first.")
        sys.exit(1)

    if args.reflect:
        reflect()
    elif args.query:
        interactive(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
