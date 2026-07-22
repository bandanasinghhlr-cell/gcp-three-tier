from flask import Flask, render_template, request, redirect
from database.mongo import students
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route("/")
def home():

    data = students.find()

    return render_template("index.html", students=data)


@app.route("/add", methods=["POST"])
def add():

    name = request.form.get("name")
    email = request.form.get("email")

    students.insert_one({

        "name": name,
        "email": email

    })

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):

    students.delete_one({

        "_id": ObjectId(id)

    })

    return redirect("/")


@app.route("/edit/<id>")

def edit(id):

    student = students.find_one({

        "_id": ObjectId(id)

    })

    return render_template("edit.html", student=student)


@app.route("/update/<id>", methods=["POST"])

def update(id):

    students.update_one(

        {

            "_id": ObjectId(id)

        },

        {

            "$set": {

                "name": request.form.get("name"),
                "email": request.form.get("email")

            }

        }

    )

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
