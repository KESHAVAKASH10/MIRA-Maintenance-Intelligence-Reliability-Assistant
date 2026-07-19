import re

def calculate_confidence(distances):
    if not distances:
        return 0.0
    avg = sum(1 - d for d in distances) / len(distances)
    return round(avg * 100, 1)


def get_confidence_label(score):
    if score >= 70:
        return "High"
    elif score >= 55:
        return "Medium"
    else:
        return "Low"


def format_sources(metadatas):
    sources = []
    seen = set()

    for meta in metadatas:
        source = f"{meta['filename']} | Page {meta['page_number']}"

        if source not in seen:
            sources.append(source)
            seen.add(source)

    return sources


def detect_equipment_tag(question):
    pattern = r"\b[A-Z]+-[A-Z]\d+\b"
    matches = re.findall(pattern, question.upper())
    return matches[0] if matches else None