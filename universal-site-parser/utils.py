import datetime, dateparser
from urllib.parse import urlparse
from tzlocal import get_localzone


class LinksChecker:
    def __init__(self, site_link: str, link_for_check: str, links: list):
        self.link_for_check = link_for_check
        self.links = links
        self.site_link = site_link

    def relative_links_to_absolute(self):
        if 'https://www.' in str(self.link_for_check['href']):
            for i in range(len(self.links)):
                self.links[i] = self.links[i]['href']


        else:
            for i in range(len(self.links)):
                relative_path = self.links[i]['href']
                self.links[i] = urlparse(self.site_link)._replace(path=relative_path).geturl()

class GetNewsLinks:
    def __init__(self, div_class_with_links_db, soup):
        self.div_class_with_links_db = div_class_with_links_db
        self.soup = soup
        self.all_articles_links = []

    def get_news_links(self):
        blocks_with_tag_a = self.soup.find_all('div', {"class": self.div_class_with_links_db})
        for block in blocks_with_tag_a:
            self.all_articles_links += block.find_all('a')
        return self.all_articles_links


class GetNewsTitle:
    def __init__(self, title_class_db, soup):
        self.title_class_db = title_class_db
        self.soup = soup

    def get_title(self):
        article = self.soup.find('article', {'class': self.title_class_db})
        title = article.find('h1').text.strip()
        return title


class GetNewsContent:
    def __init__(self, content_class_db, soup):
        self.content_class_db = content_class_db
        self.soup = soup
        self.all_content= ''

    def get_content(self):
        contents = self.soup.find('div', {'class': self.content_class_db})
        p_contents = contents.find_all('p')

        for content in p_contents:
            self.all_content += content.text
        return self.all_content.strip()


class NewsDateTime:
    def __init__(self, time_published_db, soup):
        self.time_published_db = time_published_db
        self.soup = soup

    def get_date_time(self):
        time_div = self.soup.find('div', {'class': self.time_published_db})
        time_published_str = time_div.find('time')['datetime']
        item_datetime = dateparser.parse(time_published_str, date_formats=['%Y %m %d']).date()
        return item_datetime

    def get_item_unix_time(self):
        time_div = self.soup.find('div', {'class': self.time_published_db})
        time_published_str = time_div.find('time')['datetime']
        item_unix_time = int(datetime.datetime.fromisoformat(time_published_str).timestamp())
        return item_unix_time

    def get_current_unix_upload_time(self):
        now = datetime.datetime.now(tz=get_localzone())
        item_add_unix_time = int(datetime.datetime.fromisoformat(now.strftime('%Y-%m-%d %H:%M:%S')).timestamp())
        return item_add_unix_time




