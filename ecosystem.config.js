const path = require("path");

module.exports = {
  apps: [
    {
      name: "bk-reports-backend",
      script: "poetry",
      args: "run uvicorn api.main:app --port 8080",
      interpreter: "none",
      env: {
        PYTHONUNBUFFERED: "1",
        PYTHONPATH: path.join(__dirname, "src")
      }
    },
    {
      name: "bk-reports-bot",
      script: "poetry",
      args: "run python -m bot.main",
      cwd: __dirname,
      interpreter: "none",
      env: {
        PYTHONUNBUFFERED: "1",
        PYTHONPATH: path.join(__dirname, "src")
      }
    }
  ]
}