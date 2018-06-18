from django.http import JsonResponse

from categories.models import Brand, Category, SubA, SubB


def json_selector(id_generic, id_pertain, value_generic):
        json_object = {}
        if id_pertain == 'id_category':
            query = SubA.objects.filter(category=id_generic)
        elif id_pertain == 'id_subA':
            query = SubB.objects.filter(subA=id_generic)
            if not query.exists():
                query = Brand.objects.filter(suba__pk=value_generic)
                if query.exists():
                    json_object['1'] = 0
        elif id_pertain == 'id_subB':
            query = SubC.objects.filter(subB=id_generic)
            if not query.exists():
                query = Brand.objects.filter(subb__pk=value_generic)
                if query.exists():
                    json_object['1'] = 0
        for G in query:
            json_object[int(G.id)] = str(G)
        return JsonResponse(json_object)
