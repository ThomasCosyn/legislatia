import chromadb


def build_collection(collection_name,
                     chunks,
                     embedding_function):
    chroma_client = chromadb.PersistentClient()
    collection = chroma_client.get_or_create_collection(
        collection_name,
        embedding_function=embedding_function
        )
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks
    )
    return collection
