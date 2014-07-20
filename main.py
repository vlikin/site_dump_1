import mysql.connector

langcode_list = ['en', 'ru', 'uk']

db = mysql.connector.Connect(user='root', password='', database='shelepen')
cursor = db.cursor()

# Get page nodes.
query = '''
    SELECT
	    *
    FROM
	    node n
    WHERE n.type = 'page'
'''
cursor.execute(query)
page_list =  dict((y[0][1], dict(y)) for y in [zip(['nid', 'uuid', 'vid', 'type'], x) for x in cursor.fetchall()] )

# Get article list.
query = '''
    SELECT
	    *
    FROM
	    node__field_article nfa
'''
cursor.execute(query)
article_list =  [dict(y) for y in [zip(['bundle', 'deleted', 'entity_id', 'revision_id', 'langcode', 'delta', 'field_article_target_id', 'field_article_revision_id'], x) for x in cursor.fetchall()] ]
print article_list

for key, page in page_list.items():
    print page

# Get page data.
