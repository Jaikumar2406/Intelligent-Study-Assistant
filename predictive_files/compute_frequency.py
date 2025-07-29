from collections import Counter 
import re
import load_pyq_from_pdf

def compute_frequency(syllabus, pyq_pdf_path):
    freq = {unit: Counter({t: 0 for t in topics}) for unit, topics in syllabus.items()}
    pyqs = load_pyq_from_pdf(pyq_pdf_path)
    for unit, questions in pyqs.items():
        for q in questions:
            for topic in syllabus.get(unit, []):
                if re.search(r'\b' + re.escape(topic) + r'\b', q, re.IGNORECASE):
                    freq[unit][topic] += 1
    return freq