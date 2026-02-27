from fastapi.responses import JSONResponse

def HTTPSuccess(data: dict = {}):
    data["ok"] = True
    return JSONResponse(content={"status": "success", "data": data}, status_code=200)

def HTTPError(error_name, code, error_data = None):
    data = {"status": "error", "error": error_name, "code": code}
    if error_data:
        data["details"] = error_data
    return JSONResponse(content=data, status_code=code)