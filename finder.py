import fake_useragent
import requests, time
from bs4 import BeautifulSoup
from database import dbconnection
from utils import LinksChecker, GetNewsTitle, GetNewsContent, NewsDateTime, GetNewsLinks



site_links = dbconnection.execute_site_links_from_table(db_name='resource', cell='resource_url')

def parser():


    for site in site_links:
        print(site[0])
        site_link = site[0]
        lst_news = []


        user = fake_useragent.UserAgent().random
        header = {'user-Agent': user}
        response = requests.get(site_link, headers=header).text
        soup = BeautifulSoup(response, 'lxml')

        db_links_path = dbconnection.execute_from_table(db_name='resource', cell='top_tag',
                                                                  filter_var=site_link, where='resource_url')

        all_articles_links = GetNewsLinks(db_links_path, soup).get_news_links()
        LinksChecker(site_link=site_link,
                     links=all_articles_links).relative_links_to_absolute()



        for a in all_articles_links:
            try:
                site_id = dbconnection.execute_from_table(db_name='resource', cell='RESOURCE_ID',
                                                          filter_var=site_link, where='resource_url')
                print(f'1.SITE_ID = {site_id}')

            except:
                print('Can not find site_id')

            link = a
            print(f'2.LINK = {link}')

            try:
                response = requests.get(a, headers=header).text
                time.sleep(1)
                soup = BeautifulSoup(response, 'lxml')
                time.sleep(1)
            except:
                print('failed to follow the link')

            try:
                db_title_path = dbconnection.execute_from_table(db_name='resource', cell='title_cut', filter_var=site_link,
                                                                 where='resource_url')
                title = GetNewsTitle(db_title_path, soup).get_title()
                print(f'3.TITLE: {title}')
            except:
                print('Can not find the title of the news')

            try:
                db_content_path = dbconnection.execute_from_table(db_name='resource', cell='bottom_tag',
                                                                   filter_var=site_link, where='resource_url')
                all_content = GetNewsContent(db_content_path, soup).get_content()
                print(f'4.CONTENT: {all_content}')
            except:
                print('Can not find the content of the news')

            try:
                db_time_path = dbconnection.execute_from_table(db_name='resource', cell='date_cut',
                                                                    filter_var=site_link, where='resource_url')
                item_datetime = NewsDateTime(db_time_path, soup).get_date_time()
                print(f'5.DATETIME: {item_datetime}')

                item_unix_time = NewsDateTime(db_time_path, soup).get_item_unix_time()
                print(f'6.UNIXTIME: {item_unix_time}')

                item_add_unix_time = NewsDateTime(db_time_path, soup).get_current_unix_upload_time()
                print(f'7.ADDTIME: {item_add_unix_time}')
                print()

            except:
                print('Can not find time of the news')

            else:
                lst_news.append((site_id, str(link), title, all_content, item_unix_time, item_add_unix_time, item_datetime))

        dbconnection.insert_into_table(db_name='items', collection=lst_news)
        lst_news.clear()

if __name__ == "__main__":
    parser()
