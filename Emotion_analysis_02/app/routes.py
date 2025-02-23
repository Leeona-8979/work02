from flask import render_template, request, jsonify
from crawlers.attraction.amap_provider import AMapAttractionProvider
from crawlers.attraction.data_cleaner import clean_attraction_data
from config.settings import config


def init_routes(app):
    # 初始化高德接口
    amap_provider = AMapAttractionProvider(config.AMAP_WEB_KEY)

    @app.route('/attractions')
    def list_attractions():
        """获取所有景点数据"""
        try:
            raw_data = amap_provider.get_attractions()
            cleaned_data = clean_attraction_data(raw_data)
            return jsonify({
                "status": "success",
                "data": cleaned_data
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
