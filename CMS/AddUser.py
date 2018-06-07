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
    sql = "SELECT * FROM user WHERE username ='%s'" % username
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

            user_id = cursor.lastrowid
            # execute the SQL query
            cursor.execute("select name,user_group_id From user_group")
            # fetch the data
            data = cursor.fetchall()
            i = 0
            while i < event["number_of_groups"]:
                for row in data:
                    if event["group" + str(i)] != row[0]:
                        continue
                    else:
                        addUserToGroup = ("INSERT INTO user_group_user "
                                          "(user_id,user_group_id) "
                                          "VALUES ('%s', '%s')")%(user_id, row[1])
                        cursor.execute(addUserToGroup)
                        cnx.commit()
                i+=1
            else:
                return "The user is already existed"
    else:
        return "The email is not valid"


main({'username': "suh", 'first_name': "samar", 'last_name': "fares", 'email': "samar@sdjf.sdok",
      'password': "samaroussama", 'is_group_admin': 0, 'type': 2,'group0':"bla bla bla",'number_of_groups':1}, "")
