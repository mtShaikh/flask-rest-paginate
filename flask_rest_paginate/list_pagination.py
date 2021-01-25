class ListPagination:
    def __init__(self, list_):
        self.list_ = list_

    @property
    def next_num(self):

        self.last_page = 1 + self.pages - 1
        if self.page < self.last_page:
            return self.page + 1
        else:
            return None

    @property
    def prev_num(self):
        if self.page > 1:
            return self.page - 1
        else:
            return None

    @property
    def has_next(self):
        last = (self.page - 1) * self.per_page + self.per_page
        return last < len(self.list_)

    @property
    def has_prev(self):
        first = (self.page - 1) * self.per_page
        return first > 0

    @property
    def pages(self):
        return ((len(self.list_) - 1) // self.per_page) + 1

    @property
    def total(self):
        return len(self.list_)

    def paginate(self, **kwargs):
        first = (self.page - 1) * self.per_page
        last = first + self.per_page
        self.items = self.list_[first:last]


def paginate(query_model, **kwargs):
    type = ListPagination(query_model)
    type.page = kwargs.get("page")
    type.per_page = kwargs.get("per_page")
    type.paginate()
    return type