from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.parse import quote


class CtripCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()

    # 修改为根据景点名称搜索
    def crawl_comments(self, attraction_name):
        self.driver.get(f"https://you.ctrip.com/searchsite/?query={quote(attraction_name)}")
        time.sleep(2)

        # 原有评论解析逻辑（保留你的XPath）
        comments = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        for item in soup.select('div.commentItem'):
            comments.append({
                'text': item.select_one('.commentDetail').text.strip(),
                'score': float(item.select_one('.score').text),
                'photos': [img['src'] for img in item.select('img')]
            })
        return comments
