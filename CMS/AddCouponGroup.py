import config

cnx = config.cnx

cursor = config.cursor


def alreadyExists(name):
    sql = "SELECT * FROM coupon_group WHERE name ='%s'" % name
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    if "name" in event:
        alreadyExist = alreadyExists(event["name"])

        if not alreadyExist:
            addCouponGroup = ('INSERT INTO coupon_group '
                              '(name)'
                              'VALUES ("%s")') % event["name"]

            cursor.execute(addCouponGroup)
            cnx.commit()

            print("The coupon group is added")
        else:
            print("The coupon group  is already existed")
    else:
        print("group name is required")


main(
    {'name': "customer care"}, "")
