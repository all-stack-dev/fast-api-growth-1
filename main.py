from project.settings import App

app = App()

@app.get("/echo")
async def echo():
    return {"message": "Hello World"}