import config

cnx = config.cnx
cursor = config.cursor
def exists(table,column, value):
    sql = ("SELECT * FROM %s WHERE %s = '%s'") % (table,column, value)
    cursor.execute(sql)
    x = cursor.fetchall()
    if not x:
        return False
    else:
        return True

exists("user_group", "name", "hdhs")