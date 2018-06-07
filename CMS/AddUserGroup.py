import re

import config

cnx = config.cnx

cursor = config.cursor


def main(event, context):
    add_quota_value = ("INSERT INTO quota "
                       "(type,amount) "
                       "VALUES ('%s','%s')") % (event["type"], event["amount"])
    add_quota_number = ("INSERT INTO quota "
                        "(type,number_of_coupons) "
                        "VALUES ('%s','%s')") % (event["type"], event["amount"])

    if (event["type"] == "user_level_value") | (event["type"] == "group_level_value"):
        cursor.execute(add_quota_value)
        cnx.commit()
        print(event["type"])
    else:
        cursor.execute(add_quota_number)
        cnx.commit()

    quota_id = cursor.lastrowid

    add_user_group = ("INSERT INTO user_group "
                      "(name,quota_id) "
                      "VALUES ('%s','%s')") % (event["name"], quota_id)
    cursor.execute(add_user_group)
    cnx.commit()

    ####################

    user_group_id = cursor.lastrowid

    cursor.execute("select name,coupon_group_id From coupon_group")
    # fetch the data
    data = cursor.fetchall()
    for row in data:
        if event[row[0]] is None:
            continue
        else:
            add_user_group_coupon_group = ("INSERT INTO user_group_coupon_group "
                                           "(user_group_id,coupon_group_id) "
                                           "VALUES ('%s','%s')") % (user_group_id, row[1])
            cursor.execute(add_user_group_coupon_group)
            cnx.commit()

    ########################

    cursor.execute("select name,permission_id From permission")
    # fetch the data
    data = cursor.fetchall()
    for row in data:
        if event[row[0]] is None:
            continue
        else:
            add_user_group_permission = ("INSERT INTO user_group_permission "
                                         "(user_group_id,permission_id) "
                                         "VALUES ('%s','%s')") % (user_group_id, row[1])
            cursor.execute(add_user_group_permission)
            cnx.commit()

    ########################

    i = 1
    while i < len(event):
        add_user_group_user = ("INSERT INTO user_group_user "
                               "(user_group_id,user_id) "
                               "VALUES ('%s','%s')") % (user_group_id, event["employee" + str(i)])
        cursor.execute(add_user_group_user)
        cnx.commit()
        i += 1


main({'name': "bla bla bla", 'type': "user_level_number", 'amount': "60", 'Employees Coupons': "Marketing",
      'online redeeming': "online redeeming", 'exporting': "exporting", 'employee1': 7}, "")
