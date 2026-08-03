from providers.markitdown_provider import MarkItDownProvider

provider = MarkItDownProvider()

markdown = provider.convert("docs/az900_study_guide.pdf")

print("=" * 80)
print(markdown)
print("=" * 80)