from flask import Flask, request, render_template_string

app = Flask(__name__)

print("start")


@app.route("/")
def index():
    return render_template_string(open("map.html").read())  # HTMLファイルの内容を読み込む


@app.route("/post_coordinates", methods=["POST"])
def post_coordinates():
    data = request.json
    lat = data["lat"]
    lng = data["lng"]
    print(f"{lat}, {lng}")
    # ここで必要な処理を行う
    return "Coordinates received!"


print("finish")

if __name__ == "__main__":
    app.run(debug=True)
