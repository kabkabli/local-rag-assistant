from pathlib import Path

import markitdown
from markitdown._exceptions import FileConversionException


class MarkItDownProvider:
    """
    Wrapper around Microsoft MarkItDown.

    Responsible only for converting a document into Markdown.
    """

    def __init__(self):
        self.converter = markitdown.MarkItDown()

    def convert(self, file_path: str | Path) -> str:
        """
        Convert a document to Markdown.

        Args:
            file_path: Path to the document.

        Returns:
            Markdown text.

        Raises:
            FileNotFoundError: If the file does not exist.
            RuntimeError: If MarkItDown cannot convert the document.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        try:
            result = self.converter.convert(str(path))
            return result.text_content

        except FileConversionException as e:
            raise RuntimeError(
                f"Failed to convert '{path}'.\n{e}"
            ) from e