class JsonCleaner:
    def clean_markdown_json(self, raw_text):
        if raw_text is None:
            return ""

        text = raw_text.strip()
        lines = text.splitlines()

        if len(lines) > 0 and lines[0].startswith("```"):
            lines = lines[1:]

        if len(lines) > 0 and lines[-1].startswith("```"):
            lines = lines[:-1]

        cleaned_text = "\n".join(lines)
        cleaned_text = cleaned_text.strip()

        return cleaned_text
