import config
import CheckExists

cnx = config.cnx
cursor = config.cursor


def main(event, context):
    # checking the inputs is valid
    if ("name" or "amount"or "type" or "number_of_coupon_groups" or "number_of_methods" or "number_of_users") not in event:
        return"All fields are required"
    if any(v == "" for v in [event["name"], event["amount"]]) or any(v is None for v in [event["name"], event["amount"]]):
        return "All fields are required"

    # check that the group isn't existed
    if CheckExists.exists("user_group", "name", event["name"]):
        return "This group is already existed"

    # check that the name is alphabet or numeric
    if not all(x.isalpha() or x.isspace() or x.isdigit() for x in event["name"]):
            return "Only alphabetic characters and digits are allowed"

    # check if the name is longer than 45 characters
    if len(event["name"]) > 45:
        return "The name must be 45 characters or less"

        # check the amount is numeric
    if not event["amount"].isdigit():
        return "The amount of quota must be digits only"

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
    i = 0
    while i < event["number_of_coupon_groups"]:
        for row in data:
            if "group" + str(i) not in event:
                return "group"+i + "is required"
            if event["group" + str(i)] != row[0]:
                continue
            else:
                add_user_group_coupon_group = ("INSERT INTO user_group_coupon_group "
                                               "(user_group_id,coupon_group_id) "
                                               "VALUES ('%s', '%s')") % (user_group_id, row[1])
                cursor.execute(add_user_group_coupon_group)
                cnx.commit()
        i += 1

    ########################

    cursor.execute("select name,permission_id From permission")
    # fetch the data
    data = cursor.fetchall()

    i = 0
    while i < event["number_of_methods"]:
        for row in data:
            if "method" + str(i) not in event:
                return "method"+i + "is required"
            if event["method" + str(i)] != row[0]:
                continue
            else:
                add_user_group_permission = ("INSERT INTO user_group_permission "
                                             "(user_group_id,permission_id) "
                                             "VALUES ('%s','%s')") % (user_group_id, row[1])
                cursor.execute(add_user_group_permission)
                cnx.commit()
        i += 1

    ########################

    i = 0
    while i < event["number_of_users"]:
        if "user" + str(i) not in event:
            return "user" + i + "is required"
        add_user_group_user = ("INSERT INTO user_group_user "
                               "(user_group_id,user_id) "
                               "VALUES ('%s','%s')") % (user_group_id, event["user" + str(i)])
        cursor.execute(add_user_group_user)
        cnx.commit()
        i += 1
    return"The user group is added successfully"

print(main({'name': "rg", 'type': "user_level_number", 'amount': "60", 'number_of_coupon_groups': 1, 'group0': "Marketing",
      'number_of_methods': 2, 'number_of_users': 1, 'method0': "online redeeming", 'method1': "exporting", 'user0': 1},
     ""))
