from collections import OrderedDict
def get_match_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT yid FROM ms")
    return [row[0] for row in cursor.fetchall()]

def get_table_a_data(conn, match_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * from s_y where yid = ?", (match_id,))
    return [OrderedDict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return cursor.fetchone()

def get_table_b_data(conn, match_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT x.StrideId, x.ServiceDate, x.AdmitDateTime, x.DischDateTime, x.siteuid, x.AdmitDxCode, x.DX1Code, x.DX2Code, x.DX3Code, x.DX4Code, x.DX5Code, x.DX6Code, x.DX7Code, x.DX8Code, x.DX9Code, x.DX10Code, x.ProcCode1, x.ProcCode2, x.ProcCode3, x.ProcCode4, x.ProcCode5, x.ProcCode6, x.id, x.screenid, ms.match
                   FROM s_x x LEFT OUTER JOIN ms ON x.id = ms.xid WHERE ms.yid = ?""", (match_id,))
    return [OrderedDict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

def update_match(conn, id, match):
    cursor = conn.cursor()
    cursor.execute("UPDATE ms SET match = ? WHERE xid = ?", (match, id))
    conn.commit()
