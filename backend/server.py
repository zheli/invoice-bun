import uvicorn
import os
from dotenv import load_dotenv

_ = load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # In development, reload is useful. In production, it might be disabled,
    # but for this setup we'll keep it simple or check for env (e.g. ENV=dev)
    reload = os.getenv("ENV", "dev") == "dev"
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)
