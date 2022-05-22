# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapyScraping.items import JobOpeningItem

class FormatterPipeline:
    def process_item(self, item, spider):
        if isinstance(item, JobOpeningItem):
            adapter = ItemAdapter(item)

            if adapter.get('salary'):
                adapter['salary'] = adapter['salary'].encode().decode()
                adapter['salary'] = str(adapter['salary']).replace(' ', '')
                print(adapter['salary'])

            if adapter.get('location'):
                for ind, location in enumerate(adapter['location']):
                    adapter['location'][ind] = location.encode().decode()
                for ind, location in enumerate(adapter['location']):
                    if len(adapter['location'][ind].strip()) < 3:
                        del adapter['location'][ind]

            if adapter.get('posting_time'):
                adapter['posting_time'] = adapter['posting_time'].split(' ')[3]

            if adapter.get('additional_info'):
                adapter['additional_info'] = [info for info in adapter['additional_info'] if len(info) > 3]

        return item



class PerCompanyExportPipeline:

    abs_dir = os.path.dirname(__file__)

    def open_spider(self, spider):
        self.company_exporter = {}

    def close_spider(self, spider):
        for exporter in self.company_exporter.values():
            exporter.finish_exporting


    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        company = adapter['company']
        if company not in self.company_exporter:
            path = os.path.join(self.abs_dir, '..\job_postings', str(company + '.json'))
            print(path)
            f = open(path, 'wb')

            exporter = JsonItemExporter(f, indent=4, ensure_ascii=False, encoding='utf-8')
            exporter.start_exporting()
            self.company_exporter[company] = exporter
        return self.company_exporter[company]

    def process_item(self, item, spider):
        if isinstance(item, JobOpeningItem):
            exporter = self._exporter_for_item(item)
            exporter.export_item(item)
        return item


