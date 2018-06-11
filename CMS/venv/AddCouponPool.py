import config
import datetime
import validateCodePrefixOfCoupon

from datetime import date

cnx = config.cnx
cursor = config.cursor


# validate the code prefix of the pool if it is unique


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


# check the end date if it is before  the start date or the start date is before the current date


def checkDate(start_date_obj, end_date_obj):
    if end_date_obj > start_date_obj:
        if start_date_obj > datetime.datetime.now():
            return True
        else:
            return False
    else:
        return False


# main method to handle  service "add coupon pool"


def main(event, context):
    global end_date_obj

    # check if all attributes was arrived
    if any(v not in event for v in ["pulse_code", "unique_code_prefix", "name", "file",
                                "description", "method", "start_date", "end_date", "subcategory",
                                "minimum_threshold", "monetary_value", "category"]):
        return "All information(parameters) are required "

    # check if any of the event variable is none
    if any(v is None for v in [event["pulse_code"], event["unique_code_prefix"], event["name"], event["file"],
                               event["description"], event["method"], event["start_date"], event["subcategory"],
                               event["minimum_threshold"], event["monetary_value"], event["category"]]):
        return "All fields are required "

    # check the unique code is unique
    isUnique = validateUniqueCode(event["unique_code_prefix"])

    if isUnique:
        format_str = '%d/%m/%Y'  # The format
        try:
            start_date_obj = datetime.datetime.strptime(event["start_date"], format_str)

            # check the end date
            if event["end_date"] is not None:
                end_date_obj = datetime.datetime.strptime(event["end_date"], format_str)
                if not checkDate(start_date_obj, end_date_obj):
                    print("The end date is less than the start date ")
        except ValueError:
            raise ValueError("Incorrect data format, should be DD-MM-YYYY")

        # check that the name is alphabet
        if not all(x.isalpha() or x.isspace() or x.isdigit() for x in [event["name"],
                                                                       event["description"], event["pulse_code"],
                                                                       event["unique_code_prefix"],
                                                                       event["category"], event["subcategory"]]):
            return "Only alphabetic characters and digits are allowed"

        # check the monetary value is digit
        if not all(x.isdigit() for x in event["monetary_value"]):
            return "only digits is allowed "

        # check the minimum threshold is int and digit
        if not all(x.isdigit() or isinstance(x, int) for x in event["minimum_threshold"]):
            return "only digits and integer number are allowed"

        # check if the name is longer than 45 characters
        if (len(event["name"])  or len(event["pulse_code"]) or len(event["method"])) > 45:
            return "The length of the fields must be 45 characters or less except the description"
        # end of the checking

        # get the coupon groups
        # list for saving the coupon groups
        index = 0
        dic_coupon_group = [90]
        cursor.execute("select name,coupon_group_id from coupon_group")
        data = cursor.fetchall()
        i = 0
        while i < len(event):

            if "coupon_group" + str(i) in event:
                for row in data:
                    if event["coupon_group" + str(i)] == row[0]:
                        dic_coupon_group[index] = row[1]
                        index += 1
            i += 1

        # get the subcategory id that match with the category chosen
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
        cnx.commit()
        # insert the group coupon in database
        for x in dic_coupon_group:
            query = 'Insert into coupon_group_coupon_pool (coupon_group_id,coupon_pool_id)VALUES (%s,%s)' % (
                x, coupon_pool_id)
            cursor.execute(query)

        # import the file
        number_of_coupons = 0
        try:
            with open(event["file"], "r") as ins:
                content_of_file = []
                for line in ins:
                    content_of_file.append(line)

                for line in content_of_file:
                    code_prefix = line.split('-')[0]
                    if validateCodePrefixOfCoupon.validateCodePrefixOfCoupon(code_prefix, event["unique_code_prefix"]):
                        # insert ino database
                        # first get the code of the coupon
                        code_of_coupon = line.split("-")[1]
                        query = "insert into coupon (coupon_pool_id,code) values('%s','%s')" % (
                            coupon_pool_id, code_of_coupon)
                        cursor.execute(query)
                        cnx.commit()
                        number_of_coupons += 1

                    else:
                        return "couldn't add the coupon\n the coupon doesn't match the unique code prefix "
        except Exception as e:
            return str(e)

        # update the number of coupons added in the coupon pool
        cursor.execute("UPDATE coupon_pool SET number_of_coupons =%d where coupon_pool_id =%d" % (
            number_of_coupons, coupon_pool_id))
        cnx.commit()
        return "The coupon pool added successfully"
    else:
        return "unique code prefix is already existed"
print(main({'pulse_code': '1234', "unique_code_prefix": '906', "name": "first", "description": "xyz",
      "method": "carryOut", "category": "pizza", "subcategory": "large", "coupon_group1": "emp",
      "start_date": "12/6/2018", "end_date": "13/6/2018", "minimum_threshold": "1", "monetary_value": "14",
      "file": "test.txt"}, ""))