from one_category_links import all_links
from one_category_links import link_details
import pandas
import time

for i in link_details.find():
    all_links.update_many({'href': i['url']}, {
        '$set': {'post_date': i['post_date'], 'contents': i['contents'], 'original_tag': i['original']}})

# all_links表放到Excel中
name = '{}.xlsx'.format(time.strftime("%m%d", time.localtime()))
array = [i for i in all_links.find({}, {'_id': 0, 'page_link': 0})]
df = pandas.DataFrame(array)
df.to_excel(name)
