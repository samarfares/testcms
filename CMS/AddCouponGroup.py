import config

cnx = config.cnx

cursor = config.cursor


def alreadyExists(name):
    sql = "SELECT * FROM coupon_group WHERE name ='%s'" % name
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    if "name" in event:
        if event["name"] != "":
            if all(x.isalpha() or x.isspace() or x.isdigit() for x in event["name"]):

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
            else:
                return "only alphabetic characters and digits are allowed"

        else:
            return "The group name is required"
    else:
        return "The group name is required"


main(
    {'name': "customer care"}, "")
