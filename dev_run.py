import os

import uvicorn


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(cur_dir, "dev_config.env")

    app_dir = os.path.join(cur_dir, "src")
    os.environ["ENV_PATH"] = env_path
    uvicorn.run("src.fastapi_file_server.main:create_app", app_dir=app_dir, host="127.0.0.1", port=8080, factory=True, reload=True)