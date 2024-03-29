# Django REST Spreadsheets renderer

This project pulls work from [drf-renderer-xlsx](https://github.com/wharton/drf-renderer-xlsx) and 
[django-rest-framework-csv](https://github.com/mjumbewu/django-rest-framework-csv) aiming to combine these renderers
into a single package while fixing some of their individual quirks.

## Differences
An important use case for file export in a RESTful API is to allow the user to manipulate data using their own tools. 
While pagination is useful for endpoints where you don't need to see all the data, they don't make sense for these types
of file export. This project will handle pagination by ignoring it, serializing the entire queryset.

---

In addition, to enable CSV/XLSX on an endpoint, all that needs to be done is adding a single mixin like such:

```lang=py
from drf_spreadsheets.mixins import SpreadsheetMixIn

class YourViewSet(SpreadsheetMixIn, ModelViewSet):
    ...

```

This instead of manually overriding `renderer_classes`, or adding the renderer to the defaults. The former is clunky and 
can lead to unwanted behavior, and the latter is rarely necessary since there will be many endpoints that don't need
spreadsheet exports in most projects.

---

One regression is in XLSX styling. For the initial version of this package, no styling can be applied to generated 
XLSX files. Since this is not an essential feature for most export use-cases, it has been left as a potential future feature

## Usage

To use this package, simply add the `SpreadsheetMixIn` to a ViewSet! By default, both CSV and XLSX formats will be 
available on that view. There are six fields provided by `SpreadsheetMixIn`:
 
 |field|default|use|
 |-----|-------|---|
 |enable_csv|True|Allows CSV format to be accessed on that particular ViewSet|
 |enable_xlsx|True|Allows XLSX format to be accessed on that particular ViewSet|
 |enable_spreadsheets_on_details|False|Allows the CSV and/or XLSX renderers to be used on detail views (ie not list views)|
 |enable_renderer_defaults|True|Allows the default renderers found in api_settings to also be used. If set to false, exclusively the spreadsheet renderers will be used|
 |filename|None|Overrides the auto-generated filename of the form "\<Model name> Report" or "\<View name> Report" if no model is available|
 |spreadsheet_headers|None|Overrides the auto-generated columns with either a list or a dictionary. If it is set to be a dictionary, the keys will be columns to include and the values will be their names/labels.|
 |compact_columns|False|Renders secondary data structures as json strings instead of creating new columns for their children|
 
An alternative to providing `spreadsheet_headers` as a field through `SpreadsheetMixIn` is providing it via overriding
the `get_renderer_context()` method. For example

```lang=py
    def get_renderer_context(self):
        context = super(MyViewSet, self).get_renderer_context()
        if 'headers' in self.request.GET:
            context["spreadsheet_headers"] = self.request.GET['headers'].split(',')
        return context
```

## Contributors

* Joe Paavola - https://github.com/jpaav 
* Joshua David Thomas - https://github.com/joshuadavidthomas 
* Mike Seidle - https://github.com/indymike