import re

import config

cnx = config.cnx

cursor = config.cursor


def validateEmail(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return False
    else:
        return True


def alreadyExists(username):
    sql = "SELECT * FROM user WHERE username ='%s'"%username
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    valid = validateEmail(event["email"])
    alreadyExist = alreadyExists(event["username"])
    if valid:
        if not alreadyExist:
            # how to check this email belongs to the company
            addUser = ("INSERT INTO user "
                       "(username,first_name, last_name, email, password,is_group_admin,type) "
                       "VALUES (%s,%s, %s, %s, %s, %s,%s)")

            userData = (event["username"], event["first_name"], event["last_name"], event["email"], event["password"],
                        event["is_group_admin"], event["type"])
            cursor.execute(addUser, userData)
            cnx.commit()
            addUserToGroup = ("INSERT INTO user_group_user "
                              "(userId,userGroupId) "
                              "VALUES (%d, %d")
            user_id = cursor.lastrowid
            # execute the SQL query
            cursor.execute("select name,user_group_id From user_group")
            # fetch the data
            data = cursor.fetchall()
            for row in data:
                if event[row[0]] == None:
                    continue
                else:
                    userToGroupData = (user_id, row[1])
                    cursor.execute(addUserToGroup, userToGroupData)
                    cnx.commit()
            cnx.commit()
        else:
            return "The user is already exists"
    else:
        return "The email is not valid"




main({'username': "s", 'first_name': "samar", 'last_name': "fares", 'email': "samar@sdjf.sdok",
      'password': "samaroussama", 'is_group_admin': 0, 'type': 2}, "")
