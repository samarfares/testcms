import hashlib

import config

cnx = config.cnx

cursor = config.cursor


def main(event, context):
    if "username" in event:
        if event["username"] != "":
            if "password" in event:
                if event["password"] != "":

                    checkUser = (
                            "SELECT username,password from user where username ='%s' AND password='%s'" % (
                        event["username"], hashlib.md5(event["password"].encode('utf8')).hexdigest()))
                    cursor.execute(checkUser)
                    user = cursor.fetchall()
                    if not user:
                        return "Bad Login!!"
                    else:
                        return "logged in successfully"
                else:
                    return "The password is required"
            else:
                return "The password is required"
        else:
            if "password" in event and event["password"] != "":
                return "The username is required"
            else:
                return "The username and password are required"
    else:
        if "password" in event and event["password"] != "":
            return "The username is required"
        else:
            return "The username and password are required"


main({'username': "ossama", 'passwor': "celine"}, "")
