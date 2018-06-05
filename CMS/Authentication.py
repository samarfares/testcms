import config

cnx = config.cnx

cursor = config.cursor


def main(event,context):
    checkUser = (
        "SELECT username,password from user where username ='%s' AND password='%s'"%(event["username"],event["password"]))
    cursor.execute(checkUser)
    user=cursor.fetchall()
    if not user:
        print("Bad Login!!")
    else:
        print("WOOW")


main({'username': "s", 'password': "samaroussam"},"")
