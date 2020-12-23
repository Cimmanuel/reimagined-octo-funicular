# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from crawler.models import Influencer
from scrapy_djangoitem import DjangoItem


class InstacrawlItem(DjangoItem):
    django_model = Influencer
