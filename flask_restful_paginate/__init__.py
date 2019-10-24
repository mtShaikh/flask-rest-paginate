from importlib import util
from flask import request, url_for


class Pagination:
    DEFAULT_PAGE_SIZE = 20
    DEFAULT_PAGE_NUMBER = 1
    _page_param = 'page'
    _size_param = 'size'

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app, page_param='page', size_param='size'):
        self._page_param = page_param
        self._size_param = size_param
        app.config.setdefault('DEFAULT_PAGE_SIZE', self.DEFAULT_PAGE_SIZE)
        app.config.setdefault('DEFAULT_PAGE_NUMBER', self.DEFAULT_PAGE_NUMBER)
        app.extensions['paginate'] = self

    def paginate(self, query, schema):
        page_num = request.args.get('page', self.DEFAULT_PAGE_NUMBER)
        size = request.args.get('size', self.DEFAULT_PAGE_SIZE)
        page_obj = query.paginate(page=page_num, per_page=size)
        next_page = url_for(
            request.endpoint,
            page=page_obj.next_num if page_obj.has_next else page_obj.page,
            size=size,
            **request.view_args
        )
        prev = url_for(
            request.endpoint,
            page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
            size=size,
            **request.view_args
        )
        restful = util.find_spec('flask_restful')
        if restful:
            import flask_restful as f
        else:
            import flask_restplus as f

        return {
            'total': page_obj.total,
            'pages': page_obj.pages,
            'next': next_page,
            'prev': prev,
            'results': f.marshal(page_obj.items, schema)
        }

    def create_pagination_schema(self):
        pass
