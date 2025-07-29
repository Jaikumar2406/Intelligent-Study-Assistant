import re

def load_syllabus(path):
    syllabus = {}
    current_unit = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            m = re.match(r'^(Unit\s+\d+)\s*[:\-]?', line, re.IGNORECASE)
            if m:
                current_unit = m.group(1)
                syllabus[current_unit] = []
            elif current_unit:
                topics = [t.strip() for t in line.split(',') if t.strip()]
                syllabus[current_unit].extend(topics)
    return syllabus
