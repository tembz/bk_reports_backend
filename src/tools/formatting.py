def format_seconds(seconds: int) -> str:
    seconds = int(seconds)
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"

def format_nums(num: int):
    return f"{num:,}".replace(",", ".")