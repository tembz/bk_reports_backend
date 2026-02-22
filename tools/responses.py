def HTTPSuccess(data: dict = {}):
    data["ok"] = True
    return {"status": "success", "data": data}

def HTTPError(error_name, code):
    return {"status": "error", "error": error_name, "code": code}