from flask import request, url_for


class Pagination:
    DEFAULT_PAGE_SIZE = 20
    DEFAULT_PAGE_NUMBER = 0

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('DEFAULT_PAGE_SIZE', self.DEFAULT_PAGE_SIZE)
        app.config.setdefault('DEFAULT_PAGE_NUMBER', self.DEFAULT_PAGE_NUMBER)
        app.extensions['paginate'] = self

    def paginate(self, query, schema):
        page = request.args.get('page', self.DEFAULT_PAGE_NUMBER)
        per_page = request.args.get('page_size', self.DEFAULT_PAGE_SIZE)
        page_obj = query.paginate(page=page, per_page=per_page)
        next_page = url_for(
            request.endpoint,
            page=page_obj.next_num if page_obj.has_next else page_obj.page,
            per_page=per_page,
            **request.view_args
        )
        prev = url_for(
            request.endpoint,
            page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
            per_page=per_page,
            **request.view_args
        )

        return {
            'total': page_obj.total,
            'pages': page_obj.pages,
            'next': next_page,
            'prev': prev,
            'results': schema.dump(page_obj.items).data
        }
