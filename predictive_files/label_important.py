def label_important(count, high=3, medium=1):
    if count >= high:
        return "Very Important"
    elif count >= medium:
        return "Important"
    else:
        return "Less Important"