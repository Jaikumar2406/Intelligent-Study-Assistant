import compute_frequency
import label_important
import llm_suggestion
import llm_router
import load_pyq_from_syllabus

def important_topics(user_query):
    info = llm_router(user_query)
    syllabus_path = info.get("syllabus_path")
    pyq_pdf_path = info.get("pyq_pdf_path")
    unit = info.get("unit")

    if not all([syllabus_path, pyq_pdf_path, unit]):
        print("Could not resolve file paths or unit from LLM.")
        return []

    syllabus = load_pyq_from_syllabus(syllabus_path)
    freqs = compute_frequency(syllabus, pyq_pdf_path)
    results = []

    for topic, cnt in freqs.get(unit, {}).items():
        label = label_important(cnt)
        info = {"topic": topic, "count": cnt, "label": label}
        if cnt == 0:
            info["llm_note"] = llm_suggestion(topic, unit)
        results.append(info)

    results.sort(key=lambda x: x["count"], reverse=True)
    return results
