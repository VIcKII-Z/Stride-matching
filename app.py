from flask import Flask, render_template, request, jsonify
import db
import sqlite3 
app = Flask(__name__)

# Create a SQLite3 connection
conn = sqlite3.connect("database/match.sqlite", check_same_thread=False)

@app.route("/")
def index():
    match_ids = db.get_match_ids(conn)
    return render_template("index.html", match_ids=match_ids)

@app.route("/data/<match_id>")
def get_data(match_id):
    table_a = db.get_table_a_data(conn, match_id)
    # for i in table_a[0]:
    #     print(i)
    #     print('!!!')
    #     break
    print(table_a)
    table_b = db.get_table_b_data(conn, match_id)
    # print()
    print(table_b)
    return jsonify({"table_a": table_a, "table_b": table_b})

@app.route("/update_match", methods=["POST"])
def update_match():
    id = request.form.get("id")
    match = request.form.get("match")
    db.update_match(conn, id, match)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
