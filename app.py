from flask import Flask, render_template, request, redirect, flash
from database.mongo import students
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "studentcrudproject"


@app.route("/")
def home():
    data = students.find()
    total = students.count_documents({})
    return render_template(
        "index.html",
        students=data,
        total=total
    )


@app.route("/add", methods=["POST"])
def add():

    students.insert_one({

        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "city": request.form.get("city"),
        "phone": request.form.get("phone")

    })

    flash("Student Added Successfully", "success")

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):

    students.delete_one({

        "_id": ObjectId(id)

    })

    flash("Student Deleted Successfully", "danger")

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
                "email": request.form.get("email"),
                "city": request.form.get("city"),
                "phone": request.form.get("phone")

            }

        }

    )

    flash("Student Updated Successfully", "primary")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
