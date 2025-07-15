import datetime, dateparser
from urllib.parse import urlparse

from lxml import etree
from tzlocal import get_localzone


class LinksChecker:
    def __init__(self, site_link: str, links: list):

        self.links = links
        self.site_link = site_link

    @staticmethod
    def is_absolute(link):
        if 'http' in link:
            return True
        return False

    def relative_links_to_absolute(self):

        for i in range(len(self.links)):
            if self.is_absolute(self.links[i]):
                continue
            else:
                relative_path = self.links[i]
                self.links[i] = urlparse(self.site_link)._replace(path=relative_path).geturl()


class GetNewsLinks:
    def __init__(self, db_links_path , soup):
        self.db_links_path  = db_links_path
        self.soup = soup


    def get_news_links(self):
        dom = etree.HTML(str(self.soup))
        return dom.xpath(self.db_links_path)


class GetNewsTitle:
    def __init__(self, db_title_path, soup):
        self.db_title_path = db_title_path
        self.soup = soup

    def get_title(self):
        dom = etree.HTML(str(self.soup))
        title = dom.xpath(self.db_title_path)[0].strip()
        return title


class GetNewsContent:
    def __init__(self, db_content_path, soup):
        self.db_content_path = db_content_path
        self.soup = soup
        self.all_content = ''

    def get_content(self):
        dom = etree.HTML(str(self.soup))
        contents = dom.xpath(self.db_content_path)
        for content in contents:
            self.all_content += content
        return self.all_content.strip()


class NewsDateTime:
    def __init__(self, db_time_path, soup):
        self.db_time_path= db_time_path
        self.soup = soup

    def get_date_time(self):
        dom = etree.HTML(str(self.soup))
        time_published_str = dom.xpath(self.db_time_path)[0]
        item_datetime = dateparser.parse(time_published_str, date_formats=['%Y %m %d']).date()
        return item_datetime

    def get_item_unix_time(self):
        dom = etree.HTML(str(self.soup))
        time_published_str = dom.xpath(self.db_time_path)[0]
        item_unix_time = int(datetime.datetime.fromisoformat(time_published_str).timestamp())
        return item_unix_time

    def get_current_unix_upload_time(self):
        now = datetime.datetime.now(tz=get_localzone())
        item_add_unix_time = int(datetime.datetime.fromisoformat(now.strftime('%Y-%m-%d %H:%M:%S')).timestamp())
        return item_add_unix_time
