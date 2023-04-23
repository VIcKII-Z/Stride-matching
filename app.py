from flask import Flask, render_template, request, jsonify
import db
import sqlite3 
app = Flask(__name__)

# Create a SQLite3 connection
conn = sqlite3.connect("database/match.sqlite", check_same_thread=False)

@app.route("/")
def index():
    match_id_seen= db.get_match_ids(conn)
    print(match_id_seen)
    return render_template("index.html", match_id_seen=match_id_seen)

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

@app.route('/mark_match', methods=['POST'])
def mark_match():
    match_id = request.form.get("match_id")
    print(match_id)
    c = conn.cursor()
    c.execute('UPDATE ms SET seen = 1 - seen WHERE yid = ?', (match_id,))
    conn.commit()
    c.execute('SELECT seen FROM ms WHERE yid = ?', (match_id,))
    seen = c.fetchone()[0]
    print(seen)
    return jsonify({"success":True})
    c.execute('SELECT seen FROM ms WHERE yid = ?', (match_id,))
    seen = c.fetchone()[0]
    return jsonify({'seen': seen})

@app.route("/description", methods=["GET"])
def get_description():
    query = request.args.get("query", "")
    # Execute the query and fetch the description from the database
    # For example:
    # description = db.session.execute(query).fetchone()[0]
    colname, value = query.split('||')
    c = conn.cursor()
    if colname.startswith('DX') and value:
        value = value.replace('.', '')
        c.execute("select text from icd where code=='" + value + "'")
        description = c.fetchone()[0]
        print(description)
    elif colname.startswith('Pro') and value:
        c.execute("select * from procode where CPTCode=='" + value + "'")
        description = c.fetchone()[-1]
        print(description)
    else:
        description = ''
    return jsonify(description=description)


if __name__ == "__main__":
    app.run(debug=True)
