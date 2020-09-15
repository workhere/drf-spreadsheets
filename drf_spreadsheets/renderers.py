import csv
from abc import ABC
from io import StringIO
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response


class SpreadsheetRenderer(BaseRenderer, ABC):
    level_sep = "."

    def tablize(self, data, header=None):
        """
        Convert a list of data into a table.
        If there is a header provided to tablize it will efficiently yield each
        row as needed. If no header is provided, tablize will need to process
        each row in the data in order to construct a complete header. Thus, if
        you have a lot of data and want to stream it, you should probably
        provide a header to the renderer (via the `renderer_context`).
        """

        if data:
            # First, flatten the data (i.e., convert it to a list of
            # dictionaries that are each exactly one level deep).  The key for
            # each item designates the name of the column that the item will
            # fall into.
            data = self.flatten_data(data)

            # Get the set of all unique headers, and sort them (unless already provided).
            if not header:
                # We don't have to materialize the data generator unless we
                # have to build a header.
                data = tuple(data)
                header_fields = set()
                for item in data:
                    header_fields.update(list(item.keys()))
                header = sorted(header_fields)
            if isinstance(header, dict):
                yield [header.get(x, x) for x in header]
            else:
                yield header

            # Create a row for each dictionary, filling in columns for which the
            # item has no data with None values.
            for item in data:
                row = [item.get(key, None) for key in header]
                yield row

        elif header:
            # If there's no data but a header was supplied, yield the header.
            if isinstance(header, dict):
                yield [header.get(x, x) for x in header]
            else:
                yield header

        else:
            # Generator will yield nothing if there's no data and no header
            pass

    def flatten_data(self, data):
        """
        Convert the given data collection to a list of dictionaries that are
        each exactly one level deep. The key for each value in the dictionaries
        designates the name of the column that the value will fall into.
        """
        for item in data:
            flat_item = self.flatten_item(item)
            yield flat_item

    def flatten_item(self, item):
        if isinstance(item, list):
            flat_item = self.flatten_list(item)
        elif isinstance(item, dict):
            flat_item = self.flatten_dict(item)
        else:
            flat_item = {"": item}

        return flat_item

    def nest_flat_item(self, flat_item, prefix):
        """
        Given a "flat item" (a dictionary exactly one level deep), nest all of
        the column headers in a namespace designated by prefix.  For example:
         header... | with prefix... | becomes...
        -----------|----------------|----------------
         'lat'     | 'location'     | 'location.lat'
         ''        | '0'            | '0'
         'votes.1' | 'user'         | 'user.votes.1'
        """
        nested_item = {}
        for header, val in flat_item.items():
            nested_header = self.level_sep.join([prefix, header]) if header else prefix
            nested_item[nested_header] = val
        return nested_item

    def flatten_list(self, l):
        flat_list = {}
        for index, item in enumerate(l):
            index = str(index)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, index)
            flat_list.update(nested_item)
        return flat_list

    def flatten_dict(self, d):
        flat_dict = {}
        for key, item in d.items():
            key = str(key)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, key)
            flat_dict.update(nested_item)
        return flat_dict


class CSVRenderer(SpreadsheetRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = "text/csv"
    format = "csv"

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if renderer_context is None:
            renderer_context = {}

        if data is None:
            return ""

        if not isinstance(data, list):
            data = [data]

        header = renderer_context.get("spreadsheet_headers")

        table = self.tablize(data, header=header)
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        for row in table:
            csv_writer.writerow(row)

        return csv_buffer.getvalue()


class XLSXRenderer(SpreadsheetRenderer):
    """
    Renderer which serializes to Excel
    """

    media_type = "application/xlsx"
    format = "xlsx"

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into XLSX
        """
        if renderer_context is None:
            renderer_context = {}

        if data is None:
            return ""

        if not isinstance(data, list):
            data = [data]

        # Take header and column_header params from view
        header = renderer_context.get("spreadsheet_headers")

        table = self.tablize(data, header=header)
        wb = Workbook()
        wb.active.title = "Report Worksheet"
        for row in table:
            wb.active.append(row)

        # Save
        return save_virtual_workbook(wb)
