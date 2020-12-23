import json
from urllib.parse import urlencode

import scrapy
from django.conf import settings
from instacrawl.items import InstacrawlItem

usernames = ["niggacaspian"]


def get_url(url):
    payload = {"api_key": settings.SCRAPERAPI_API_KEY, "url": url}
    proxy_url = f"http://api.scraperapi.com/?{urlencode(payload)}"
    return proxy_url


class InstaSpider(scrapy.Spider):
    name = "instaspider"
    allowed_domains = ["api.scraperapi.com"]
    custom_settings = {"CONCURRENT_REQUESTS_PER_DOMAIN": 5}

    def start_requests(self):
        for username in usernames:
            url = f"https://www.instagram.com/{username}/?hl=en"
            yield scrapy.Request(get_url(url), callback=self.parse)

    def parse(self, response):
        raw_data = response.xpath(
            "//script[starts-with(.,'window._sharedData')]/text()"
        ).extract_first()
        json_extract = raw_data.strip().split("= ")[1][:-1]
        data = json.loads(json_extract)

        user_id = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

        edges = data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
            "edge_owner_to_timeline_media"
        ]["edges"]

        item = InstacrawlItem()

        for edge in edges:
            item["username"] = edge["node"]["owner"]["username"]

            if edge["node"]["is_video"]:
                item["picture"] = edge["node"]["video_url"]
            else:
                item["picture"] = edge["node"]["display_url"]

            yield item

        next_page_bool = data["entry_data"]["ProfilePage"][0]["graphql"][
            "user"
        ]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

        if next_page_bool:
            cursor = data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
                "edge_owner_to_timeline_media"
            ]["page_info"]["end_cursor"]
            di = {"id": user_id, "first": 12, "after": cursor}

            params = {
                "query_hash": "e769aa130647d2354c40ea6a439bfc08",
                "variables": json.dumps(di),
            }
            url = (
                f"https://www.instagram.com/graphql/query/?{urlencode(params)}"
            )

            yield scrapy.Request(
                get_url(url), callback=self.parse_pages, meta={"pages_di": di}
            )

    def parse_pages(self, response):
        di = response.meta["pages_di"]
        data = json.loads(response.text)

        edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

        item = InstacrawlItem()

        for edge in edges:
            item["username"] = edge["node"]["owner"]["username"]

            if edge["node"]["is_video"]:
                item["picture"] = edge["node"]["video_url"]
            else:
                item["picture"] = edge["node"]["display_url"]

            yield item

        next_page_bool = data["data"]["user"]["edge_owner_to_timeline_media"][
            "page_info"
        ]["has_next_page"]

        if next_page_bool:
            cursor = data["data"]["user"]["edge_owner_to_timeline_media"][
                "page_info"
            ]["end_cursor"]
            di["after"] = cursor
            params = {
                "query_hash": "e769aa130647d2354c40ea6a439bfc08",
                "variables": json.dumps(di),
            }
            url = "https://www.instagram.com/graphql/query/?" + urlencode(
                params
            )

            yield scrapy.Request(
                get_url(url), callback=self.parse_pages, meta={"pages_di": di}
            )
