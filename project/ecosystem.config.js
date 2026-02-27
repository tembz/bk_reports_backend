module.exports = {
  apps: [
    {
      name: "bk-reports-backend",
      script: "poetry",
      args: "run uvicorn src.api.main:app --port 8080",
      interpreter: "none",
      env: {
        PYTHONUNBUFFERED: "1"
      }
    },
    {
      name: "bk-reports-bot",
      script: "poetry",
      args: "run python src/bot/main.py",
      interpreter: "none",
      env: {
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
}