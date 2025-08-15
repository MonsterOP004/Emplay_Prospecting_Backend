import re

def clean_content(text: str) -> str:
    
    if not text:
        return ""

    # Remove bold/italic markers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # italic

    # Remove headings (keep content)
    text = re.sub(r'#+\s*(.*)', r'\1', text)

    # Remove extra multiple spaces
    text = re.sub(r' +', ' ', text)

    # Strip extra blank lines
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text.strip()
