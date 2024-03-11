import sqlite3

def context_from_tags(tags):
    """
    Creates a context from the given tags. Searches for courses based on the tags in data/coursesDB.db.

    :param tags: A list of class tags.
    :return: A dictionary containing the class descriptions for each tag.
    """
    results = {}
    with sqlite3.connect('data/coursesDB.db') as conn:
        cursor = conn.cursor()
        for tag in tags:
            # split the tag by spaces
            subject = tag.split()[0]
            catalog = tag.split()[1]
            # Use parameterized queries to prevent SQL injection
            sql = """
                    SELECT
                        Descr,
                        `Course Long Descr`,
                        `Mtg Start`,
                        `Mtg End`,
                        Pat,
                        `Term Descr`
                    FROM
                        courses
                    WHERE
                        `Subject` = ? AND `Catalog` = ?
                  """
            cursor.execute(sql, (subject, catalog))

            result = cursor.fetchone()
            result_dict = {
                'course name': result[0],
                'course description': result[1],
                'start time': result[2],
                'end time': result[3],
                'days offered': result[4],
                'term': result[5]
            }

            # Add result to dictionary of results
            results[tag] = result_dict

    return results