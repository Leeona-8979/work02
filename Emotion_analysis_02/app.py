# app.py

from flask import Flask, request, jsonify,send_from_directory
from pandas import Period

import Component.getSentiment
import Component.getKeyword
import Component.getComment

import os
import warnings

# 1. 修复环境变量警告
os.environ["HF_HOME"] = os.environ.get("TRANSFORMERS_CACHE", os.path.expanduser("~/.cache/huggingface"))

# 2. 忽略 transformers 的 FutureWarning
from transformers.utils import logging as transformers_logging

transformers_logging.disable_progress_bar()
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.utils.hub")

# 新增：预加载 BERT 模型
from Component.bertEncode import load_bert_model
tokenizer, bert_model = load_bert_model(device="cpu")  # 使用 CPU 或 "cuda"

app = Flask(__name__, static_folder='web')

@app.route('/')
def home():
    return "情感分析服务已启动！请访问 /getCmtCount 等接口。"

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')


# 更多静态文件目录，如 '/src/'
@app.route('/src/<path:path>')
def serve_js(path):
    return send_from_directory('web/src', path)


# 定义转换函数
def convert_period_to_str(obj):
    if isinstance(obj, dict):
        return {k: convert_period_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_period_to_str(item) for item in obj]
    elif isinstance(obj, Period):
        return str(obj)
    else:
        return obj


# 获取评论数量
@app.route('/getCmtCount', methods=['GET'])
def get_comment_count():
    count = Component.getComment.get_comment_count()
    return jsonify({'count': count})


# 获取指定IP的评论数量
@app.route('/getCmtCountByIP', methods=['GET'])
def get_comment_count_by_ip():
    ip = request.args.get('ip')
    count = Component.getComment.get_comment_count_by_ip(ip)
    return jsonify({'count': count})


# 获取指定数量IP列表，以及对应的评论数量
@app.route('/getIPList', methods=['GET'])
def get_ip_list():
    top = int(request.args.get('top'))
    ip_list = Component.getComment.get_ip_list(top)
    return jsonify(ip_list)


# 获取指定IP的评论
@app.route('/getCmtByIP', methods=['GET'])
def get_comment_by_ip():
    ip = request.args.get('ip')
    comments = Component.getComment.get_comment_by_ip(ip)
    return jsonify(comments)


# 获取指定情感的评论数量
@app.route('/getCmtCountBySentiment', methods=['GET'])
def get_comment_count_by_sentiment():
    sentiment = request.args.get('sentiment')
    count = Component.getComment.get_comment_count_by_sentiment(int(sentiment))
    return jsonify({'count': count})


# 获取指定情感的评论
@app.route('/getCmtBySentiment', methods=['GET'])
def get_comment_by_sentiment():
    sentiment = request.args.get('sentiment')
    comments = Component.getComment.get_comment_by_sentiment(int(sentiment))
    return jsonify(comments)


# 获取情感列表，以及对应的评论数量
@app.route('/getSentimentList', methods=['GET'])
def get_sentiment_list():
    sentiment_list = Component.getComment.get_sentiment_list()
    # text = request.args.get('comment')
    # # 调用 Component.getSentiment 中的函数，并传入预加载的模型
    # results = Component.getSentiment.get_sentiment(text, tokenizer, bert_model)
    return jsonify(sentiment_list)


# 获取指定数量的评论
@app.route('/getComments', methods=['GET'])
def get_comments():
    index = int(request.args.get('index'))
    end = int(request.args.get('end'))
    comments = Component.getComment.get_comments(index, end)
    return jsonify(comments)


# 获取随机评论
@app.route('/getRandomComments', methods=['GET'])
def get_random_comments():
    comment = Component.getComment.get_random_comments()
    comment = convert_period_to_str(comment)
    return jsonify(comment)


# 获取关键词
@app.route('/getKeyword', methods=['GET'])
def get_keyword():
    topK = int(request.args.get('topK'))
    keywords = Component.getKeyword.get_keyword(topK)
    return jsonify(keywords)


# 获取指定情感的关键词
@app.route('/getKeywordBySentiment', methods=['GET'])
def get_keyword_by_sentiment():
    sentiment = request.args.get('sentiment')
    topK = int(request.args.get('topK'))
    keywords = Component.getKeyword.get_keyword_by_sentiment(int(sentiment), topK)
    return jsonify(keywords)


# 获取情感
@app.route('/getSentiment', methods=['GET'])
def get_sentiment():
    # text = request.args.get('comment')
    # results = Component.getSentiment.get_sentiment(text)
    # return jsonify(results)
    text = request.args.get('comment')
    # 调用 Component.getSentiment 中的函数，并传入预加载的模型
    results = Component.getSentiment.get_sentiment(text)
    return jsonify(results)


# 获取不同时间的评论数量
@app.route('/getCmtCountByTime', methods=['GET'])
def get_comment_count_by_time():
    comment_counts = Component.getComment.get_comment_count_by_time()
    comment_counts_dict = comment_counts.index.astype(str).to_series().reset_index(drop=True).to_dict()
    counts = comment_counts.tolist()
    result = dict(zip(comment_counts_dict.values(), counts))
    return jsonify(result)


# 获取IP归属地的数量
@app.route('/getIPCount', methods=['GET'])
def get_ip_count():
    count = Component.getComment.get_ip_count()
    return jsonify({'count': count})


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=5010)
    app.run(debug=True)
