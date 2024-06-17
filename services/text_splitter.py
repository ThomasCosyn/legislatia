from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(texts):
    """
    Splits a given text into smaller chunks using a
    RecursiveCharacterTextSplitter.

    Args:
        texts (str): The text to be split.

    Returns:
        list: A list of smaller text chunks.

    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", ".", ","]
    )
    chunks = splitter.split_text(texts)
    return chunks
