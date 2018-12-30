from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class itemCsvExporter(CsvItemExporter):

    def __int__(self, *args, **kwargs):
        #delimiter = settings.get('CSV_DELIMITER',',')

        fields_to_export = settings.get('FIELDS_TO_EXPORT',[])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(itemCsvExporter, self).__init__(*args, **kwargs)