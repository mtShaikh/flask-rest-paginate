from importlib import util
from collections import OrderedDict
from flask import request, url_for
import flask_restful as f


class Pagination:
    DEFAULT_PAGE_NUMBER = 1
    _default_page_size = 20
    _page_param = 'page'
    _size_param = 'size'
    _resource_links_enabled = True

    def __init__(self, app=None, db=None):
        if app is not None:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        self._db = db
        self._page_param = app.config.setdefault('PAGINATE_PAGE_PARAM', 'page')
        self._size_param = app.config.setdefault('PAGINATE_SIZE_PARAM', 'size')
        self._default_page_size = app.config.setdefault('PAGINATE_PAGE_SIZE', 20)
        self._resource_links_enabled = app.config.setdefault('PAGINATE_RESOURCE_LINKS_ENABLED', True)
        app.extensions['paginate'] = self

    def paginate(self, query_model, schema, marshmallow=False, post_query_hook=None):
        """
        paginate the query
        :param query_model:
        Query object

        :param schema:
        Marshmallow Schema or Flask reqparse schema

        :param marshmallow:
        Flag to indicate schema param is a Marshmallow Schema object

        :param post_query_hook:
        function to be called on data fetched by the query. It can be
        used to execute operations on the queried data
        The function takes one argument: `func(data: List)` which is the list of retrieved objects
         from the db and must returns a list containing the objects

        """
        def _is_integer(num):
            if num is not None and num.isdigit():
                return True

        query_page = request.args.get(self._page_param)
        query_size = request.args.get(self._size_param)

        if _is_integer(query_page):
            page_num = int(query_page)
        else:
            page_num = self.DEFAULT_PAGE_NUMBER

        if _is_integer(query_size):
            size = int(query_size)
        else:
            size = self._default_page_size

        # TODO: linked to db exception
        # if Model, run the default query
        if isinstance(query_model, type(self._db.Model)):
            # `error_out` makes it so that it doesnt throw a 404 when page_num is
            # above total page limit
            page_obj = query_model.query.paginate(page=page_num, per_page=size, error_out=False)
        else:
            # this will be a BaseQuery instance, and so we can call paginate directly
            page_obj = query_model.paginate(page=page_num, per_page=size, error_out=False)

        prev_page = None
        next_page = None
        if self._resource_links_enabled:
            def _get_page_link(page_number=None):
                if page_number is not None:
                    request.view_args[self._page_param] = page_number

                return url_for(request.endpoint, **request.view_args)

            request.view_args = dict(**request.view_args, **request.args.to_dict())

            request.view_args[self._size_param] = page_obj.per_page

            current_page = _get_page_link(page_obj.page)

            if page_obj.has_next:
                next_page = _get_page_link(page_obj.next_num)

            if page_obj.has_prev:
                prev_page = _get_page_link(page_obj.prev_num)

        else:
            if page_obj.has_prev:
                prev_page = page_obj.prev_num
            if page_obj.has_next:
                next_page = page_obj.next_num

            current_page = page_obj.page

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

        items = page_obj.items
        if post_query_hook:
            items = post_query_hook(page_obj.items)
        if not items:
            raise ValueError("Incorrect signature")

        return {
            # TODO: use a better name for the pagination object
            'pagination': OrderedDict(sorted(pagination_schema.items())),
            'data': schema.dump(items, many=True) if marshmallow else f.marshal(page_obj.items, schema)
        }

    # TODO: make the pagination schema configurable
    def create_pagination_schema(self):
        pass
