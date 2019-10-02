from product.models import Product
from django.core.paginator import Paginator


class AbstractCategory:
    def __init__(self, request, categories=None):
        self.categories = categories
        self.search = request.GET.get('results', None)
        self.min_price = request.GET.get('min', None)
        self.max_price = request.GET.get('max', None)
        self.status = request.GET.get('status', None)
        self.brand = request.GET.get('brand', None)
        # Paginator
        self.page = request.GET.get('page', None)

    def _resolve_categories(self):
        if not self.categories:
            return {}

        categories = {}
        for k, v in self.categories.items():
            categories["{}__{}".format(k, "slug")] = v.slug
        return categories

    def resolve_filter_by(self):
        filter_by = self._resolve_categories()
        for attr, val in self.__dict__.items():
            if val:
                if attr == 'min_price':
                    filter_by['price__gte'] = int(val)
                elif attr == 'max_price':
                    filter_by['price__lte'] = int(val)
                elif attr == 'status':
                    filter_by['status'] = val
                elif attr == 'brand':
                    filter_by['brand__slug'] = val
                else:
                    pass
        return filter_by

    def resolve_products(self):
        filter_by = self.resolve_filter_by()
        products = Product.actives.custom_filter(self.search, filter_by)
        paginator = Paginator(products, 2)
        return paginator.get_page(self.page)

    def resolve_path(self):
        path = []
        for c, (attr, val) in enumerate(sorted(self.categories.items())):
            if c == 0:
                path.append([val])
            else:
                j = list(path[c-1])
                j.append(val)
                path.append(j)
        return path

    def resolve_quantity_products(self):
        return len(self.resolve_products())
