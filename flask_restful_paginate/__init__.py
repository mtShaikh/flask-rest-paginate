from importlib import util
from collections import OrderedDict
from flask import request, url_for


class Pagination:
    DEFAULT_PAGE_NUMBER = 1
    _default_page_size = 20
    _page_param = 'page'
    _size_param = 'size'
    _resource_links_enabled = True

    def __init__(self, app=None, db=None):
        if app is not None:
            self.app = app

            # TODO: rewrite the exception
            if db is None:
                raise Exception('Provide the db object along with app in Paginate Extension')

            self._db = db
            self.init_app(app)

    def init_app(self, app):
        self._page_param = app.config.setdefault('PAGINATE_PAGE_PARAM', 'page')
        self._size_param = app.config.setdefault('PAGINATE_SIZE_PARAM', 'size')
        self._default_page_size = app.config.setdefault('PAGINATE_PAGE_SIZE', 20)
        self._resource_links_enabled = app.config.setdefault('PAGINATE_RESOURCE_LINKS_ENABLED', True)
        app.extensions['paginate'] = self

    def paginate(self, query_model, schema):
        # TODO: refactor string to integer checking/conversion
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

        # if Model, run the default query
        if isinstance(query_model, type(self._db.Model)):
            # `error_out` makes it so that it doesnt throw a 404 when page_num is
            # above total page limit
            page_obj = query_model.query.paginate(page=page_num, per_page=size, error_out=False)
        else:
            # this will be a BaseQuery instance, and so we can call paginate directly
            page_obj = query_model.paginate(page=page_num, per_page=size, error_out=False)

        # TODO: refactor this whole bit
        prev_page = None
        next_page = None
        if self._resource_links_enabled:
            request.view_args = {**request.view_args, **request.args.to_dict()}

            request.view_args[self._size_param] = page_obj.per_page

            request.view_args[self._page_param] = page_obj.page
            current_page = url_for(
                request.endpoint,
                **request.view_args
            )

            if page_obj.has_next:
                request.view_args[self._page_param] = page_obj.next_num
                next_page = url_for(
                    request.endpoint,
                    **request.view_args
                )

            if page_obj.has_prev:
                request.view_args[self._page_param] = page_obj.prev_num
                prev_page = url_for(
                    request.endpoint,
                    **request.view_args
                )

        else:
            if page_obj.has_prev:
                prev_page = page_obj.prev_num
            if page_obj.has_next:
                next_page = page_obj.next_num

            current_page = page_obj.page

        restful = util.find_spec('flask_restful')
        if restful:
            import flask_restful as f
        else:
            import flask_restplus as f

        # TODO: make the pagination schema configurable
        pagination_schema = {
            'hasNext': page_obj.has_next,
            'hasPrev': page_obj.has_prev,
            'currentPage': current_page,
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
