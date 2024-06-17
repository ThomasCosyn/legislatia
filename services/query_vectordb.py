def query_collection(collection, query):
    """
    Query the collection with a given query.

    Args:
        collection: The collection to query.
        query: The query text.

    Returns:
        The results of the query.
    """
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results
