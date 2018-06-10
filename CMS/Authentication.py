import hashlib

import config

cnx = config.cnx

cursor = config.cursor


def main(event, context):
    if "username" in event:
        if "password" in event:

            checkUser = (
                    "SELECT username,password from user where username ='%s' AND password='%s'" % (
                event["username"], hashlib.md5(event["password"].encode('utf8')).hexdigest()))
            cursor.execute(checkUser)
            user = cursor.fetchall()
            if not user:
                print("Bad Login!!")
            else:
                print("logged in successfully")
        else:
            print("password is required")
    else:
        if "password" in event:
            print("username is required")
        else:
            print("username and password are required")


main({'usernam': "", 'password': "celine"}, "")
