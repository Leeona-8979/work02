import folium
import jieba.analyse
from pyecharts import options as opts
from pyecharts.charts import WordCloud


def generate_heatmap(attractions):
    """生成地理热力图（复用你的情感分数）"""
    quzhou_center = [28.942, 118.874]
    m = folium.Map(location=quzhou_center, zoom_start=11)
    for attr in attractions:
        folium.CircleMarker(
            location=attr['location'][::-1],  # 高德坐标转标准GPS
            radius=attr['avg_score'] * 2,
            color='#ff0000',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
    return m._repr_html_()


def generate_wordcloud(comments):
    """生成情感关键词词云（使用你原有的分词逻辑）"""
    words = jieba.analyse.extract_tags(' '.join(comments), topK=50)
    return (
        WordCloud()
        .add("", words)
        .set_global_opts(title_opts=opts.TitleOpts(title="评论高频词"))
    ).render_embed()
