from rest_framework.response import Response
from rest_framework.settings import api_settings

from drf_spreadsheets.renderers import CSVRenderer, XLSXRenderer, SpreadsheetRenderer


class SpreadsheetMixIn:
    """
    A MixIn that allows a viewset to serialize list data as CSV or Excel
    """

    enable_csv = True

    enable_xlsx = True

    filename = None

    def __init__(self, *args, **kwargs):
        classes = []
        if self.enable_csv and CSVRenderer not in self.renderer_classes:
            classes.append(CSVRenderer)
        if self.enable_xlsx and XLSXRenderer not in self.renderer_classes:
            classes.append(XLSXRenderer)
        self.renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + classes
        super(SpreadsheetMixIn, self).__init__()

    def paginate_queryset(self, queryset):
        """
        Only paginates queryset if it is not a SpreadsheetRenderer. Otherwise, we should retain all records.
        """
        if isinstance(self.request.accepted_renderer, SpreadsheetRenderer):
            return None
        else:
            return super(SpreadsheetMixIn, self).paginate_queryset(queryset)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Return the response with the proper content disposition and the customized
        filename instead of the browser default (or lack thereof).
        """
        response = super(SpreadsheetMixIn, self).finalize_response(
            request, response, *args, **kwargs
        )
        filename = (
            self.filename
            if self.filename is not None
            else f"{self.model.__name__} Report"
        )
        if isinstance(response, Response):
            if response.accepted_renderer.format == "xlsx":
                response[
                    "content-disposition"
                ] = f"attachment; filename={filename}.xlsx"
            elif response.accepted_renderer.format == "csv":
                response["content-disposition"] = f"attachment; filename={filename}.csv"
        return response
