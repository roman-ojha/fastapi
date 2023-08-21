from fastapi import FastAPI
import uvicorn

app = FastAPI()
PORT = 8080

# Docs: https://www.uvicorn.org/#running-programmatically


@app.get('/')
async def index():
    return "Hello World"


if __name__ == "__main__":
    # To config and run the app without reload
    # uvicorn.run(app=app, host="127.0.0.1", port=PORT)

    # Another Way
    # config = uvicorn.Config(app=app, port=8080)
    # server = uvicorn.Server(config=config)
    # server.run()

    # Configure and run app with reload for that we have to provide application as import string
    uvicorn.run("main:app", port=PORT, reload=True)

# Now you can use 'python main.py' command
