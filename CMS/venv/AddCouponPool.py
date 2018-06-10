import config
import datetime
from datetime import date

cnx = config.cnx

cursor = config.cursor


def validateUniqueCode(code):
    query = "select unique_code_prefix from coupon_pool"
    cursor.execute(query)
    data = cursor.fetchall()
    i = 0
    for row in data:
        if row[i] == code:
            return False
        i += 1
    return True


def checkDate(start_date_obj, end_date_obj):
    if end_date_obj > start_date_obj:
        if start_date_obj > datetime.datetime.now():
            return True
        else:
            return False
    else:
        return False


def validateCodePrefix(code, unique_code_prefix):
    if code == unique_code_prefix:
        return True
    else:
        return False


def main(event, context):
    isunique = validateUniqueCode(event["unique_code_prefix"])
    if isunique:
        format_str = '%d/%m/%Y'  # The format
        start_date_obj = datetime.datetime.strptime(event["start_date"], format_str)
        end_date_obj = datetime.datetime.strptime(event["end_date"], format_str)
        if event["end_date"] is not None:

            if not checkDate(start_date_obj, end_date_obj):
                print("The end date is less than the start date ")

        # get the coupon groups
        # list for saving the coupon groups
        print("else of end checking")
        index = 0
        dic_coupon_group = [90]
        cursor.execute("select name,coupon_group_id from coupon_group")
        data = cursor.fetchall()
        for row in data:
            if event["coupon_grouprow[0]] is None:
                continue
            else:
                dic_coupon_group[index] = row[1]
                index += 1

        query = ("SELECT subcategory_id from subcategory join category where subcategory.name='%s' and "
                 "category.name ='%s'" % (event["subcategory"], event["category"]))
        cursor.execute(query)
        subcategory_id = cursor.fetchall()

        # insert the coupon pool in the database

        addCouponPool = "INSERT INTO coupon_pool (pulse_code,unique_code_prefix, name, description, method," \
                        "start_date,end_date,minimum_threshold,monetary_value,subcategory_id," \
                        "number_of_coupons) VALUES ('%s','%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s'," \
                        "'%s')" % (event["pulse_code"], event["unique_code_prefix"], event["name"],
                                   event["description"], event["method"], start_date_obj, end_date_obj,
                                   event["minimum_threshold"], event["monetary_value"], subcategory_id[0][0], 0)
        cursor.execute(addCouponPool)
        coupon_pool_id = cursor.lastrowid
        print(coupon_pool_id)
        cnx.commit()
        # insert the group coupon in database
        for x in dic_coupon_group:
            query = 'Insert into coupon_group_coupon_pool (coupon_group_id,coupon_pool_id)VALUES (%s,%s)' % (
                x, coupon_pool_id)
            cursor.execute(query)

        # import the file
        number_of_coupons = 0
        with open("test.txt", "r") as ins:
            content_of_file = []
            for line in ins:
                content_of_file.append(line)

            for line in content_of_file:
                code_prefix = line.split('-')[0]
                if validateCodePrefix(code_prefix, event["unique_code_prefix"]):
                    # insert ino database
                    # first get the code of the coupon
                    code_of_coupon = line.split("-")[1]
                    print(code_of_coupon)
                    query = "insert into coupon (coupon_pool_id,code) values('%s','%s')" % (
                        coupon_pool_id, code_of_coupon)
                    cursor.execute(query)
                    cnx.commit()
                    number_of_coupons += 1
                    print(number_of_coupons)
                else:
                    print("couldn't add the coupon\n the coupon doesn't match the unique code prefix ")
        cursor.execute("UPDATE coupon_pool SET number_of_coupons ='%s'where coupon_pool_id='%s'" % (
            number_of_coupons, coupon_pool_id))
    else:
        print("unique code prefix is already exists")


main({'pulse_code': '1234', "unique_code_prefix": '906', "name": "first", "description": "xyz",
      "method": "carryOut", "category": "pizza", "subcategory": "large", "coupon_group": "emp",
      "start_date": "8/6/2018", "end_date": "10/6/2018", "minimum_threshold": 1, "monetary_value": 14,
      "file": "test.txt", }, "")
