import uvicorn
import webbrowser
from threading import Timer

if __name__ == "__main__":
    Timer(1.5, lambda: webbrowser.open("http://localhost:8000/docs")).start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
