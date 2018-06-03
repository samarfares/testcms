import re
import config


cnx = config.cnx

cursor = config.cursor


def validateEmail(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        return False
    else:
        return True


def main(event, context):
    valid = validateEmail(event["email"])
    if valid:
      # """query for the email checking"""
        addUser = ("INSERT INTO users "
                   "(first_name, last_name, email, password,isAdmin,type) "
                   "VALUES (%s, %s, %s, %s, %s)")
        addUserToGroup = ("INSERT INTO UserToGroup "
                          "(userId,userGroupId) "
                          "VALUES (%d, %d")

        userData = (event["firstName"], event["lastName"], event["email"], event["password"], event["isAdmin"], "2")
        cursor.execute(addUser, userData)

        # execute the SQL query
        cursor.execute("select userGroupName,userGroupId From UserGroup")
         #fetch the data
        data = cursor.fetchall()
        for row in data:
         if event[row[0]]==None:
             continue
         else:
             cursor.execute("select userId From Users where email="+event["email"])
             userId=cursor.fetchall()
             userToGroupData = { row[1], userId}
             cursor.execute(addUserToGroup, userToGroupData)






    cnx.commit()

    cursor.close()
