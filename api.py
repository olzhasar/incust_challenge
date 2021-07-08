from factory import create_app

app = create_app()


@app.route("/")
def home():
    return {"hello": "world"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
