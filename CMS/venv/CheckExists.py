def alreadyExists(username):
    sql = "SELECT * FROM user WHERE username ='%s'" % username
    cursor.execute(sql)
    return cursor.fetchall()