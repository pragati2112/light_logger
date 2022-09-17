import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from uvicorn.config import LOGGING_CONFIG

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    num_workers = int(os.getenv('WORKERS')) if os.getenv('WORKERS') is not None else 1
    app_port = int(os.getenv('APP_PORT')) if os.getenv('APP_PORT') is not None else 8001
    should_reload = False
    if os.getenv('APP_ENV') == 'dev':
        should_reload = True

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run("server.app:app",
                host="0.0.0.0",
                port=app_port,
                reload=should_reload,
                workers=num_workers)
