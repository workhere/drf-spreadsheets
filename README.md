# Django REST Spreadsheets renderer

This project pulls work from [drf-renderer-xlsx](https://github.com/wharton/drf-renderer-xlsx) and 
[django-rest-framework-csv](https://github.com/mjumbewu/django-rest-framework-csv) aiming to combine these renders into
a single package while fixing some of their individual quirks.

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

This instead of manually overriding renderer_classes, or adding the renderer to the defaults. The former is clunky and 
can lead to unwanted behavior and the latter is rarely necessary since there will be many endpoints that don't need
spreadsheet exports in most projects.

---

One regression is in XLSX styling. For the initial version of this package, no styling can be applied to generated 
XLSX files. Since this is not an essential feature for most export use-cases, it has been left as a potential future feature

