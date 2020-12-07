from rest_framework.response import Response
from rest_framework.settings import api_settings

from drf_spreadsheets.renderers import CSVRenderer, XLSXRenderer, SpreadsheetRenderer


class SpreadsheetMixIn:
    """
    A MixIn that allows a REST view to serialize list data as CSV or Excel
    """

    # If set to True, the CSVRenderer will be made available in the view this MixIn is added to
    enable_csv = True

    # If set to True, the XLSXRenderer will be made available in the view this MixIn is added to
    enable_xlsx = True

    # If set to True, the renderers provided by this MixIn will be available on views marked as "details".
    # This is particularly useful for ViewSets, where the list view should have spreadsheet capabilities,
    # but the single record detail should not.
    enable_spreadsheets_on_details = False

    # If set to True, the default renderers found in api_settings.DEFAULT_RENDERER_CLASSES will be preserved as options
    # for the view this MixIn is added to. Setting this to false should only be done for spreadsheet only endpoints.
    enable_renderer_defaults = True

    # Setting filename will override the default naming system, which take the model or viewset name and appends
    # ' Report' and the file extension. You do not need to include the file extension in this parameter, it will be
    # automatically resolved for you.
    filename = None

    # Setting spreadsheet_headers to a list will override which columns are included in the spreadsheet. Setting it to
    # a dictionary will allow renaming of headers from their original field names. For example:
    #   spreadsheet_headers = {'id': 'id', 'full_name': 'name'}
    # will include just the id and full_name fields as columns and will use 'name' as the column header instead of the
    # default 'full_name'. If this field is set to None (default value), all fields will be used in alphabetical order.
    spreadsheet_headers = None

    # Setting compact_columns to True will cause lists and dictionaries to be serialized into strings instead of separate
    # columns.
    compact_columns = False

    def __init__(self, *args, **kwargs):
        if not kwargs["detail"] or self.enable_spreadsheets_on_details:
            classes = []
            if self.enable_csv:
                classes.append(CSVRenderer)
            if self.enable_xlsx:
                classes.append(XLSXRenderer)
            if self.enable_renderer_defaults:
                self.renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + classes
            else:
                self.renderer_classes = classes
        super(SpreadsheetMixIn, self).__init__()

    def get_renderer_context(self):
        """
        Overrides renderer_context with the spreadsheet_headers field if they exist
        """
        context = super(SpreadsheetMixIn, self).get_renderer_context()
        if self.spreadsheet_headers:
            context["spreadsheet_headers"] = self.spreadsheet_headers
        context["compact_columns"] = self.compact_columns
        return context

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

        if isinstance(response.accepted_renderer, SpreadsheetRenderer):
            # Resolve filename, either from override, model, or view name
            if self.filename is not None:
                filename = self.filename
            elif self.model is not None:
                filename = f"{self.model.__name__} Report"
            else:
                filename = f"{self.get_view_name()} Report"

            # Only add Content-Disposition if the renderer is XLSX or CSV
            if response.accepted_renderer.format == "xlsx":
                response[
                    "Content-Disposition"
                ] = f"attachment; filename={filename}.xlsx"
            elif response.accepted_renderer.format == "csv":
                response["Content-Disposition"] = f"attachment; filename={filename}.csv"
        return response
