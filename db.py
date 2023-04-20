from collections import OrderedDict
def get_match_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT yid, seen FROM ms")
    id_seen = {}
    for id, seen in cursor.fetchall():
        id_seen[id] = seen
    return id_seen

def get_table_a_data(conn, match_id):
    cursor = conn.cursor()
    cursor.execute("SELECT screenid, which_fuint, item_index, fall_injurybonebreak, fall_dislocatedjoint, fall_injuryhead, fall_cutbleeding, fall_cutbleeding_close, fall_sprainstrain, fall_bruiseswell, fall_otherinjury, fall_bonebrk_1, fall_bonebrk_2, fall_bonebrk_3, fall_bonebrk_4, fall_bonebrk_5, fall_bonebrk_6, fall_bonebrk_7, fall_bonebrk_8, fall_bonebrk_9, fall_bonebrk_10, fall_bonebrk_11, fall_bonebrk_12, fall_bonebrk_13, fall_bonebrk_14, fall_bonebrk_15, fall_bonebrk_16, fall_bonebrk_17, fall_bonebrk_18, fall_bonebrk_19, fall_bonebrk_20, fall_bonebrk_21, fall_er_date, fall_doctor_date, fall_otherfacility_date, fall_overnighthosp_date, siteuid, event, id from s_y where yid = ?", (match_id,))
    return [OrderedDict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

def get_table_b_data(conn, match_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT x.StrideId, x.ServiceDate, x.AdmitDateTime, x.DischDateTime, x.siteuid, x.AdmitDxCode, x.DX1Code, x.DX2Code, x.DX3Code, x.DX4Code, x.DX5Code, x.DX6Code, x.DX7Code, x.DX8Code, x.DX9Code, x.DX10Code, x.ProcCode1, x.ProcCode2, x.ProcCode3, x.ProcCode4, x.ProcCode5, x.ProcCode6, x.id, x.screenid, ms.match
        FROM s_x x LEFT OUTER JOIN ms ON x.id = ms.xid WHERE ms.yid = ?
    """, (match_id,))

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return [OrderedDict(zip(columns, row)) for row in rows]

def update_match(conn, id, match):
    cursor = conn.cursor()
    cursor.execute("UPDATE ms SET match = ? WHERE xid = ?", (match, id))
    conn.commit()
