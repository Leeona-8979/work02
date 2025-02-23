import requests


class AMapAttractionProvider:
    def __init__(self, api_key):
        self.base_url = "https://restapi.amap.com/v3/place/text"
        self.api_key = api_key

    def get_attractions(self, city="衢州"):
        """获取指定城市的所有景点"""
        params = {
            "keywords": "景点",
            "city": city,
            "key": self.api_key,
            "offset": 50,
            "extensions": "all",
            "output": "json"
        }

        response = requests.get(self.base_url, params=params)
        return self._parse_response(response.json())

    def _parse_response(self, data):
        """解析高德API响应"""
        attractions = []
        for poi in data.get("pois", []):
            attractions.append({
                "id": poi["id"],
                "name": poi["name"],
                "location": list(map(float, poi["location"].split(','))),
                "photos": [photo["url"] for photo in poi.get("photos", [])],
                "address": poi["address"]
            })
        return attractions
