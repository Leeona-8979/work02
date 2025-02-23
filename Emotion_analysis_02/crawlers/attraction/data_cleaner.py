# -*- coding: utf-8 -*-
from analysis.sentiment import batch_analyze

def clean_attraction_data(raw_attractions):
    """清洗景点信息"""
    required_fields = ["id", "name", "location"]
    return [attr for attr in raw_attractions
            if all(field in attr for field in required_fields)]


def process_comments(raw_comments):
    """处理评论数据并添加情感分析"""
    return batch_analyze([
        {
            "text": comment.get("text", ""),
            "rating": comment.get("rating", 0),
            "source": "meituan"
        }
        for comment in raw_comments
    ])
