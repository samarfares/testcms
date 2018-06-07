import config

cnx = config.cnx

cursor = config.cursor


def alreadyExists(name):
    sql = "SELECT * FROM coupon_group WHERE name ='%s'" % name
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    alreadyExist = alreadyExists(event["name"])

    if not alreadyExist:
        addCouponGroup = ('INSERT INTO coupon_group '
                          '(name)'
                          'VALUES ("%s")') % event["name"]

        cursor.execute(addCouponGroup)
        cnx.commit()

        return "The coupon group is added"
    else:
        return "The coupon group  is already existed"


main(
    {'name': "customer care"}, "")
