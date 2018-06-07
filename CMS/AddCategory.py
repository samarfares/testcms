import config

cnx = config.cnx

cursor = config.cursor


def alreadyExists(name):
    sql = "SELECT * FROM category WHERE name ='%s'" % name
    cursor.execute(sql)
    return cursor.fetchall()


def main(event, context):
    alreadyExist = alreadyExists(event["name"])

    if not alreadyExist:
        addCategory = ('INSERT INTO category '
                       '(name)'
                       'VALUES ("%s")') % event["name"]

        # categoryData = (event["name"])
        cursor.execute(addCategory)
        cnx.commit()
        category_id = cursor.lastrowid
        addAnySubCategory = 'INSERT INTO subcategory (category_id,name)VALUES ("%s","%s")' % (category_id, "any")

        cursor.execute(addAnySubCategory)
        cnx.commit()
        i = 1
        while i < len(event):
            addSubCategory = 'INSERT INTO subcategory (category_id,name)VALUES ("%s","%s")' % (
                category_id, event['subcategory' + str(i)])
            cursor.execute(addSubCategory)
            cnx.commit()
            i += 1
        return "The category is added"
    else:
        return "The category is already existed"


main(
    {'name': "l", 'subcategory1': "large", 'subcategory2': "medium", 'subcategory3': "small", 'subcategory4': "la3eeh"},
    "")
