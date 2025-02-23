# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class MeituanScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    def get_comments(self, poi_id):
        """根据美团景点ID获取评论"""
        url = f"https://www.meituan.com/poi/{poi_id}/"
        self.driver.get(url)

        # 点击"全部评论"
        self.driver.find_element(By.CSS_SELECTOR, ".comment-tab-nav li:nth-child(2)").click()
        time.sleep(1)

        comments = []
        # 滚动加载（示例加载5页）
        for _ in range(5):
            items = self.driver.find_elements(By.CSS_SELECTOR, ".comment-item")
            for item in items:
                try:
                    comments.append({
                        "text": item.find_element(By.CSS_SELECTOR, ".content").text,
                        "rating": float(
                            item.find_element(By.CSS_SELECTOR, ".star").get_attribute("style").split(":")[1].replace(
                                "%", "")) / 20
                    })
                except Exception as e:
                    continue
            self.driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)

        return comments
