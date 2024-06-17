from langchain_community.document_loaders import UnstructuredURLLoader


def load_html(urls):
    """
    Load HTML content from a list of URLs.

    Args:
        urls (list): A list of URLs to load HTML content from.

    Returns:
        str: The concatenated HTML content from all the URLs.
    """
    loader = UnstructuredURLLoader(urls)
    data = loader.load()
    if len(data) > 0:
        return data[0].page_content
    return ""
