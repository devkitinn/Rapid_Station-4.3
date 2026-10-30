#import pymssql
import wx
import wx.grid
import psycopg2
import conf
import decimal

def connect():
    conf.get_conf()
    conn = psycopg2.connect(
        host=conf.config.get('POSTGRESQL', 'host'),
        database=conf.config.get('POSTGRESQL', 'database'),
        user=conf.config.get('POSTGRESQL', 'user'),
        password=conf.config.get('POSTGRESQL', 'password'),
    )
    return conn

# ------------------------------
# Division-aware read helper
# ------------------------------

def _division_where_clause(table_alias: str = "db_part"):
    allowed = conf.get_allowed_divisions() # e.g. ['Q','V','O']
    if 'O' in allowed:
        return "", []
    groups = []
    params = []
    if 'Q' in allowed:
        groups.append(f"({table_alias}.jobname LIKE %s OR {table_alias}.jobname LIKE %s)")
        params.extend(["Q%", "RQ%"])
    if 'V' in allowed:
        groups.append(f"({table_alias}.jobname LIKE %s OR {table_alias}.jobname LIKE %s)")
        params.extend(["V%", "RV%"])
    if not groups:
        groups.append(f"({table_alias}.jobname LIKE %s OR {table_alias}.jobname LIKE %s OR {table_alias}.jobname LIKE %s OR {table_alias}.jobname LIKE %s)")
        params.extend(["Q%", "RQ%", "V%", "RV%"])
    where = " AND (" + " OR ".join(groups) + ")"
    return where, params

# ------------------------------
# READ QUERIES (division-aware)
# ------------------------------

def getPartsByRapidLocation(recutLocationNumber):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid FROM db_part "
            " LEFT JOIN db_nsjob ON db_part.jobname=db_nsjob.name "
            " WHERE lid = %s AND partmaterial != 'Mel_16_Pbd_HMR' "
            + div_where +
            " ORDER BY jobinstalldate"
        )
        cursor.execute(sql, [recutLocationNumber] + div_params)
        data = cursor.fetchall()
        return [row[0] for row in data]
    finally:
        if conn:
            conn.close()

def getAllRapids():
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, partmaterial, db_nsjob.jobinstalldate FROM db_part "
            " LEFT JOIN db_nsjob ON db_part.jobname=db_nsjob.name "
            " WHERE lid > 0 AND rapid = '1' AND partmaterial != 'Mel_16_Pbd_HMR' "
            + div_where +
            " ORDER BY jobinstalldate"
        )
        cursor.execute(sql, div_params)
        data = cursor.fetchall()
        return [row[0] for row in data]
    finally:
        if conn:
            conn.close()

def getAllPartsWithRapids():
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, db_part.jobname, workorder, partname, cabnum, cabname, partmaterial, partlength, partwidth, "
            "partthickness, partbandingstring, lid, updated, rid, trolleyslot, jobinstalldate, current_timestamp "
            "FROM db_part "
            "LEFT JOIN db_nsjob ON db_part.jobname=db_nsjob.name "
            "WHERE lid > 0 AND lid IS NOT NULL AND partmaterial != 'Mel_16_Pbd_HMR' "
            + div_where +
            " ORDER BY db_nsjob.jobinstalldate, partid"
        )
        cursor.execute(sql, div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getPartsWithRapids(rapidCol):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT DISTINCT ON (partid) partid, db_part.jobname, workorder, partname, cabnum, cabname, partmaterial, partlength, partwidth, "
            "partthickness, partbandingstring, lid, updated, rid, trolleyslot, jobinstalldate, current_timestamp "
            "FROM db_part "
            "LEFT JOIN db_nsjob ON db_part.jobname=db_nsjob.name "
            "WHERE lid = %s AND partmaterial != 'Mel_16_Pbd_HMR' "
            + div_where +
            " ORDER BY partid, db_nsjob.jobinstalldate"
        )
        cursor.execute(sql, [rapidCol] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getPart(partID):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        cursor.execute(
            (
                "SELECT "
                "db_part.partid, db_part.jobname, db_part.workorder, "  # 0, 1, 2
                "db_part.partname, db_part.cabnum, db_part.cabname, "   # 3, 4, 5
                "db_part.partmaterial, db_part.partlength, db_part.partwidth, "  # 6, 7, 8
                "db_part.partthickness, db_part.partbandingstring, db_part.lid, " # 9, 10, 11
                "db_part.rid, db_part.updated, db_part.trolleyslot, " # 12, 13, 14
                "db_part.notes, "                                   # 15
                "db_nsjob.jobinstalldate, "                         # 17
                "db_part.partintbandingmaterial, "                   # 18
                "db_part.partcomment "                               # 19
                "FROM db_part LEFT JOIN db_nsjob ON db_part.jobname=db_nsjob.name "
                "WHERE db_part.partid = %s;"
            ),
            [partID]
        )
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getPrintParts(jobName):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, jobname, workorder, partname, cabnum, cabname, partmaterial, partlength, "
            "partwidth, partthickness FROM db_part "
            "WHERE jobname LIKE %s "
            + div_where
        )
        cursor.execute(sql, [f"{jobName}%"] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getJobRapidParts(jobName):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, partid, partname, cabnum, cabname, partmaterial, partlength, partwidth, "
            "partbandingstring, lid FROM db_part WHERE jobname LIKE %s "
            + div_where
        )
        cursor.execute(sql, [f"{jobName}%"] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getJobRapids(jobName):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, partid, workorder, partname, cabnum, cabname, partmaterial, partlength, partwidth, "
            "partthickness, partbandingstring, lid, jobname FROM db_part WHERE jobname LIKE %s "
            + div_where +
            " ORDER BY cabnum"
        )
        cursor.execute(sql, [f"{jobName}%"] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getJobInstallDate(jobName):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_nsjob")
        sql = (
            "SELECT jobname, jobinstalldate FROM db_nsjob WHERE jobname LIKE %s "
            + div_where
        )
        cursor.execute(sql, [f"{jobName}%"] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

def getLocationRapidParts(recutLocationNumber):
    conn, cursor = connect(), None
    try:
        cursor = conn.cursor()
        div_where, div_params = _division_where_clause("db_part")
        sql = (
            "SELECT partid, jobname, partid, partname, cabnum, cabname, partmaterial, partlength, partwidth, "
            "partbandingstring FROM db_part WHERE lid = %s AND partmaterial != 'Mel_16_Pbd_HMR' "
            + div_where
        )
        cursor.execute(sql, [recutLocationNumber] + div_params)
        data = cursor.fetchall()
        return [row for row in data]
    finally:
        if conn:
            conn.close()

# ------------------------------
# WRITE QUERIES (no division filter)
# ------------------------------

def updateRapidPart(partid, jobname, workorder, partname, cabnum, cabname,
                    partmaterial, partlength, partwidth, partthickness,
                    partbandingstring, lid, rid, trolleyslot, notes,
                    partintbandingmaterial=None, partcomment=None):
    sql = (
        "UPDATE db_part SET jobname=%s, workorder=%s, partname=%s, cabnum=%s, cabname=%s, "
        "partmaterial=%s, partlength=%s, partwidth=%s, partthickness=%s, partbandingstring=%s, "
        "lid=%s, rid=%s, trolleyslot=%s, notes=%s, partintbandingmaterial=%s, partcomment=%s, updated=NOW() "
        "WHERE partid=%s"
    )
    params = [jobname, workorder, partname, cabnum, cabname,
              partmaterial, partlength, partwidth, partthickness,
              partbandingstring, lid, rid, trolleyslot, notes,
              partintbandingmaterial, partcomment, partid]
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, params)
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def moveRapid(partid, nextStation):
    sql = "UPDATE db_part SET lid=%s, updated=NOW() WHERE partid=%s"
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [nextStation, partid])
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def setTool(partid, rid):
    sql = "UPDATE db_part SET rid=%s, updated=NOW() WHERE partid=%s"
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [rid, partid])
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def setBay(partid, bay):
    sql = "UPDATE db_part SET trolleyslot=%s, updated=NOW() WHERE partid=%s"
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [bay, partid])
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def setPartRapidReason(partid, reasonid, nextStation):
    sql = "UPDATE db_part SET rapid=1, reasonid=%s, lid=%s, updated=NOW() WHERE partid=%s"
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [reasonid, nextStation, partid])
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def makeRapidPart(partid, nextStation, reasonid=None):
    sql = "UPDATE db_part SET rapid=1, lid=%s, reasonid=COALESCE(%s, reasonid), updated=NOW() WHERE partid=%s"
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [nextStation, reasonid, partid])
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

# def addRapidMulti(parts, nextStation):
#     sql = "UPDATE db_part SET rapid=1, lid=%s, updated=NOW() WHERE partid=%s"
#     conn = connect(); cur = conn.cursor()
#     try:
#         for pid in parts:
#             cur.execute(sql, [nextStation, pid])
#         conn.commit(); return True
#     except Exception:
#         conn.rollback(); raise
#     finally:
#         conn.close()

# def makeRapidMulti(parts, reasonid, nextStation):
#     sql = "UPDATE db_part SET rapid=1, reasonid=%s, lid=%s, updated=NOW() WHERE partid=%s"
#     conn = connect(); cur = conn.cursor()
#     try:
#         for pid in parts:
#             cur.execute(sql, [reasonid, nextStation, pid])
#         conn.commit(); return True
#     except Exception:
#         conn.rollback(); raise
#     finally:
#         conn.close()

def makeRapidMulti(scannedID, jobName, workorder, partname, cabnum, cabname, material, finallength, finalwidth, thickness, bandinglabelcode, station):
    sql = (
        "UPDATE db_part SET jobname=%s, workorder=%s, partname=%s, cabnum=%s, cabname=%s, "
        "partmaterial=%s, partlength=%s, partwidth=%s, partthickness=%s, partbandingstring=%s, "
        "rapid=1, lid=%s WHERE partid=%s"
    )
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [jobName, workorder, partname, cabnum, cabname,
                          material, finallength, finalwidth, thickness,
                          bandinglabelcode, station, scannedID])
        conn.commit()
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

def addRapidMulti(scannedID, jobname, workorder, partname, cabnum, cabname, material, finallength, finalwidth, thickness, bandinglabelcode, station):
    sql = (
        "INSERT INTO db_part (partid, partqty, jobname, workorder, partname, cabnum, cabname, "
        "partmaterial, partlength, partwidth, partthickness, partbandingstring, lid, "
        "partdescription, grain, rapid, reasonid, created, updated) "
        "VALUES (%s, 1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
        "'Rapid Rework Part', 0, 1, 0, current_timestamp, current_timestamp)"
    )
    conn = connect(); cur = conn.cursor()
    try:
        cur.execute(sql, [scannedID, jobname, workorder, partname, cabnum, cabname,
                          material, finallength, finalwidth, thickness, bandinglabelcode, station])
        conn.commit()
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()


# ----------------------------------------------
# NEW: Create a cloned RAPID part with 'R' prefix
#      (idempotent without ON CONFLICT) + partqty
# ----------------------------------------------

def createRapidClone(new_id, original_row, nextStation, reasonid=None):
    """
    Create or update a cloned RAPID part from an existing part row.
    - If a row with partid=new_id exists, update lid/reasonid/updated.
    - Otherwise insert a fresh clone with created=NOW(), updated=NOW(), partqty=1.
    Works even if db_part has no unique index on partid.
    """
    conn = connect(); cur = conn.cursor()
    try:
        # 1) Try UPDATE first
        update_sql = (
            "UPDATE db_part SET lid=%s, reasonid=COALESCE(%s, reasonid), updated=NOW() "
            "WHERE partid=%s"
        )
        cur.execute(update_sql, [nextStation, reasonid, new_id])
        if cur.rowcount and cur.rowcount > 0:
            conn.commit(); return True
        # 2) No existing row -> INSERT (set partqty=1)
        insert_sql = (
            "INSERT INTO db_part (partid, jobname, workorder, partname, cabnum, cabname, "
            "partmaterial, partlength, partwidth, partthickness, partbandingstring, lid, rid, trolleyslot, notes, rapid, reasonid, "
            "created, updated, partintbandingmaterial, partcomment, partqty) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1,%s, NOW(), NOW(), %s, %s, 1)"
        )
        params = [
            new_id,
            original_row[1],  # jobname
            original_row[2],  # workorder
            original_row[3],  # partname
            original_row[4],  # cabnum
            original_row[5],  # cabname
            original_row[6],  # partmaterial
            original_row[7],  # partlength
            original_row[8],  # partwidth
            original_row[9],  # partthickness
            original_row[10], # partbandingstring
            nextStation,      # lid
            original_row[12], # rid
            original_row[14], # trolleyslot
            original_row[15], # notes
            reasonid,         # reasonid
            original_row[18] if len(original_row) > 18 else None, # partintbandingmaterial
            original_row[19] if len(original_row) > 19 else None  # partcomment
        ]
        cur.execute(insert_sql, params)
        conn.commit(); return True
    except Exception:
        conn.rollback(); raise
    finally:
        conn.close()

# Ensure configuration is loaded
conf.get_conf()
