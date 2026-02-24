def HTTPSuccess(data: dict = {}):
    data["ok"] = True
    return {"status": "success", "data": data}

def HTTPError(error_name, code, error_data = None):
    data = {"status": "error", "error": error_name, "code": code}
    if error_data:
        data["details"] = error_data
    return data