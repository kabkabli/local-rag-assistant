from pathlib import Path
from markitdown import MarkItDown


class MarkItDownProvider:
    """
    Wrapper around Microsoft's MarkItDown library.

    Responsible only for converting a document into Markdown.
    """

    def __init__(self):
        self.converter = MarkItDown()

    def convert(self, file_path: str | Path) -> str:
        """
        Convert a supported document to Markdown.

        Args:
            file_path: Path to the document.

        Returns:
            Markdown text.
        """

        result = self.converter.convert(str(file_path))

        return result.text_content