from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# ===== Dogクラス =====
class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def to_dict(self):
        return {"name": self.name, "breed": self.breed, "age": self.age}

# ===== データ操作関数 =====
def load_dogs(filename="dogs.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {k: Dog(**v) for k, v in data.items()}
    except FileNotFoundError:
        return {}

def save_dogs(dogs, filename="dogs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({k: d.to_dict() for k, d in dogs.items()}, f, indent=2, ensure_ascii=False)

dogs = load_dogs()

# ===== ルーティング =====
@app.route("/")
def index():
    return render_template("index.html", dogs=dogs)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip().lower()
    breed = request.form["breed"].strip()
    age = request.form["age"].strip()

    if name and breed and age.isdigit() and name not in dogs:
        dogs[name] = Dog(name, breed, int(age))
        save_dogs(dogs)
    return redirect("/")

# ===== 実行エントリーポイント =====
if __name__ == "__main__":
    app.run(debug=True)

