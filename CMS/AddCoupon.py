# Feed into existing
import config
import validateCodePrefixOfCoupon

cnx = config.cnx
cursor = config.cursor


def main(event, context):
    # check if unique code prefix is arrived and not none
    if "unique_code_prefix" in event and "file" in event:
        # check if the event is not none
        if event["unique_code_prefix"] is not None and event["file"] is not None:
            # get the id of the coupon pool chosen
            sql = "select coupon_pool_id from coupon_pool where unique_code_prefix='%s'" % event["unique_code_prefix"]
            cursor.execute(sql)
            coupon_pool_id = cursor.fetchall()
            cnx.commit()
            try:
                # import the file and get each coupon
                myFile = open(event["file"], "r")
                number_of_coupons = 0
                for line in myFile:
                    code_prefix = line.split('-')[0]
                    # check the code prefix of the coupon if it is matching the code prefix of coupon pool
                    if validateCodePrefixOfCoupon.validateCodePrefixOfCoupon(code_prefix, event["unique_code_prefix"]):
                        # insert ino database
                        # first get the code of the coupon
                        code_of_coupon = line.split("-")[1]
                        query = "insert into coupon (coupon_pool_id,code) values('%s','%s')" % (
                            coupon_pool_id[0][0], code_of_coupon)
                        cursor.execute(query)
                        cnx.commit()
                        # increment the number of the coupons
                        number_of_coupons += 1
                    else:
                        return "couldn't add the coupon\n the coupon doesn't match the unique code prefix "
            except Exception as e:
                return str(e)

            # update the number of coupons added in the coupon pool
            cursor.execute("UPDATE coupon_pool SET number_of_coupons ='%s' where coupon_pool_id ='%s'" % (
                number_of_coupons, coupon_pool_id))
            cnx.commit()
            return "the coupon added successfully"
        else:
            return "All fields are required"
    else:
        return "All information(parameters) are required "

print(main({"unique_code_prefix":'906', "file":"test.txt"},""))