import unicodedata

def normalize_filename(filename):
    normalized = unicodedata.normalize(
        'NFKD', filename
    ).encode(
        'ascii', 'ignore'
    ).decode(
        'utf-8'
    )
    return normalized.replace(" ", "_")