
# check if the code prefix of the coupon is matching the code prefix of the coupon pool

import config

cnx = config.cnx
cursor = config.cursor


def validateCodePrefixOfCoupon(code, unique_code_prefix):
    if code == unique_code_prefix:
        return True
    else:
        return False
