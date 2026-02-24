module.exports = {
    apps: [
      {
        name: "bk-reports-backend",
        script: "poetry",
        args: "run uvicorn src.main:app --port 8080",
        interpreter: "none",
        env: {
          PYTHONUNBUFFERED: "1"
        }
      }
    ]
  }