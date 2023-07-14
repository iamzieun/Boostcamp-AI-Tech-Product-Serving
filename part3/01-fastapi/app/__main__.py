if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
    # reload=True: 변경사항이 있을 때마다 다시 로드
