from importlib import util
from collections import OrderedDict
from flask import request, url_for


class Pagination:
    DEFAULT_PAGE_NUMBER = 1
    _default_page_size = 20
    _page_param = 'page'
    _size_param = 'size'

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        self._page_param = app.config.setdefault('PAGINATE_PAGE_PARAM', 'page')
        self._size_param = app.config.setdefault('PAGINATE_SIZE_PARAM', 'size')
        self._default_page_size = app.config.setdefault('PAGINATE_PAGE_SIZE', 20)
        app.extensions['paginate'] = self

    def paginate(self, query, schema):
        # TODO: refactor this
        query_page = request.args.get(self._page_param)
        query_size = request.args.get(self._size_param)

        if query_page is not None and query_page.isdigit():
            query_page = int(query_page)
        else:
            query_page = self.DEFAULT_PAGE_NUMBER

        if query_size is not None and query_size.isdigit():
            query_size = int(query_size)
        else:
            query_size = self._default_page_size

        page_num = query_page or self.DEFAULT_PAGE_NUMBER
        size = query_size or self._default_page_size

        # `error_out` makes it so that it doesnt throw a 404 when page_num is
        # above total page limit
        page_obj = query.paginate(page=page_num, per_page=size, error_out=False)

        # TODO: make the URL persist the filter values
        # TODO: construct URL using the page and size param names
        # TODO: make it configurable so that I can get only next page number rather than the whole URL
        # TODO: refactor the next/prev page logic
        prev_page = None
        next_page = None
        if page_obj.has_next:
            next_page = url_for(
                request.endpoint,
                page=page_obj.next_num,
                size=size,
                **request.view_args
            )

        if page_obj.has_prev:
            prev_page = url_for(
                request.endpoint,
                page=page_obj.prev_num,
                size=size,
                **request.view_args
            )

        restful = util.find_spec('flask_restful')
        if restful:
            import flask_restful as f
        else:
            import flask_restplus as f

        # TODO: make the pagination schema configurable
        pagination_schema = {
            'hasNext': page_obj.has_next,
            'hasPrev': page_obj.has_prev,
            'currentPage': page_obj.page,
            'pages': page_obj.pages,
            'size': page_obj.per_page,
            'totalElements': page_obj.total,
        }

        if prev_page is not None:
            pagination_schema['prev'] = prev_page
        if next_page is not None:
            pagination_schema['next'] = next_page

        return {
            # TODO: use a better name for the pagination object
            'pagination': OrderedDict(pagination_schema),
            'data': f.marshal(page_obj.items, schema)
        }

    def create_pagination_schema(self):
        pass
