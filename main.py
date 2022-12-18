import uvicorn
if __name__ == "__main__":
    uvicorn.run("mainAPI:app", host="localhost", port=8080, reload=True)