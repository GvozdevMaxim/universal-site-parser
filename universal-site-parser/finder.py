import requests, time
from bs4 import BeautifulSoup
from database import dbconnection
from constants import SITE_ID, header
from utils import LinksChecker, GetNewsTitle, GetNewsContent, NewsDateTime, GetNewsLinks

site_link = dbconnection.execute_from_table(db_name='resource', cell='resource_url',
                                            filter_var=SITE_ID, where='resource_id')
response = requests.get(site_link, headers=header).text
soup = BeautifulSoup(response, 'lxml')

div_class_with_links_db = dbconnection.execute_from_table(db_name='resource', cell='top_tag',
                                                          filter_var=site_link, where='resource_url')

all_articles_links = GetNewsLinks(div_class_with_links_db, soup).get_news_links()
LinksChecker(site_link=site_link, link_for_check=all_articles_links[0],
             links=all_articles_links).relative_links_to_absolute()

lst_news = []

for a in all_articles_links:
    link = a
    print(f'1.LINK = {link}')

    try:
        response = requests.get(a, headers=header).text
        soup = BeautifulSoup(response, 'lxml')
        time.sleep(1)
    except:
        print('failed to follow the link')

    try:
        title_class_db = dbconnection.execute_from_table(db_name='resource', cell='title_cut', filter_var=site_link,
                                                         where='resource_url')
        title = GetNewsTitle(title_class_db, soup).get_title()
        print(f'2.TITLE: {title}')
    except:
        print('Can not find the title of the news')

    try:
        content_class_db = dbconnection.execute_from_table(db_name='resource', cell='bottom_tag',
                                                           filter_var=site_link, where='resource_url')
        all_content = GetNewsContent(content_class_db, soup).get_content()
        print(f'3.CONTENT: {all_content}')
    except:
        print('Can not find the content of the news')

    try:
        time_published_db = dbconnection.execute_from_table(db_name='resource', cell='date_cut',
                                                            filter_var=site_link, where='resource_url')
        item_datetime = NewsDateTime(time_published_db, soup).get_date_time()
        print(f'4.DATETIME: {item_datetime}')

        item_unix_time = NewsDateTime(time_published_db, soup).get_item_unix_time()
        print(f'5.UNIXTIME: {item_unix_time}')

        item_add_unix_time = NewsDateTime(time_published_db, soup).get_current_unix_upload_time()
        print(f'6.ADDTIME: {item_add_unix_time}')
        print()

    except:
        print('Can not find time of the news')

    else:
        lst_news.append((SITE_ID, str(link), title, all_content, item_unix_time, item_add_unix_time, item_datetime))

dbconnection.insert_into_table(db_name='items', collection=lst_news)
lst_news.clear()
