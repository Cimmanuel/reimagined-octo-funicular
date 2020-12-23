# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.models import Influencer
from django.core.exceptions import ObjectDoesNotExist


class InstacrawlPipeline:
    def process_item(self, item, spider):
        _ = Influencer.objects.get_or_create(**item)

        return item
