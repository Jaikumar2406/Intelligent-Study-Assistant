from langchain.tools import tool

@tool
def read_txt_file(filename: str) -> str:
    """Reads a .txt file and returns the content."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

