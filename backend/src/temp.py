from modal_api import Model, app
import modal
from fastapi import FastAPI

fastapp = FastAPI()

image = modal.Image.debian_slim(python_version="3.9").pip_install(
    "fastapi",
    "uvicorn",
    "python-multipart",
    "pillow",  # for image handling
)

@fastapp.post("/infer")
def infer(request: dict):

    model = Model()
    out = model.inference.remote(prompt=request['prompt'])
    return out


@app.function(image=image, timeout=1800)
@modal.asgi_app()
def fastapi_app():
    return fastapp

# This is needed for local development
if __name__ == "__main__":
    app.serve()