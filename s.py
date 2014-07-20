from lib import get_session, prepare_files
from tables import Node, File

session = get_session()

# Pages.
page_list = session.query(Node).filter(Node.type=='page').all()
item = page_list[2]
print item
print item.field_data[0]
print item.node__field_article[0]
print item.node__field_article[0].entity

# Articles.
print 'Articles.'
item = session.query(Node).filter(Node.type=='article').all()[2]
print item
print item.node__field_image[0]
print item.node__field_image[0].file

print '--------------'
for page in page_list:
    print page
    print page.field_data
# json.dumps(item.node__field_image[0])

def prepare_files():
    print 'It processes files.'
    file_list = session.query(File).all()
    print file_list

prepare_files()