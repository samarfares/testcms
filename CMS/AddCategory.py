import config

cnx = config.cnx

cursor = config.cursor


def alreadyExists(name):
    sql = "SELECT * FROM category WHERE name ='%s'" % name
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    if "name" in event and event["name"] != "":
        if len(event["name"]) < 45:
            if all(x.isalpha() or x.isspace() or x.isdigit() for x in event["name"]):
                alreadyExist = alreadyExists(event["name"])

                if not alreadyExist:
                    addCategory = ('INSERT INTO category '
                                   '(name)'
                                   'VALUES ("%s")') % event["name"]

                    # categoryData = (event["name"])
                    cursor.execute(addCategory)
                    cnx.commit()
                    category_id = cursor.lastrowid
                    addAnySubCategory = 'INSERT INTO subcategory (category_id,name)VALUES ("%s","%s")' % (
                        category_id, "any")

                    cursor.execute(addAnySubCategory)
                    cnx.commit()
                    i = 0
                    while i < len(event):
                        if "subcategory" + str(i) in event:
                            if event["subcategory" + str(i)]!= "" :
                                addSubCategory = 'INSERT INTO subcategory (category_id,name)VALUES ("%s","%s")' % (
                                    category_id, event['subcategory' + str(i)])
                                cursor.execute(addSubCategory)
                                cnx.commit()
                        i += 1
                    print ("The category is added")
                else:
                    print ("The category is already existed")
            else:
                print ("only alphabetic characters and digits are allowed")
        else:
            print ("The name must be 45 characters or less")
    else:
        print ("The category name is required")


main(
    {'name': "qer", 'subcategory1': "large", 'subcategory2': "medium", 'subcategory3': "small",
     'subcategory4': "la3eeh"},
    "")
