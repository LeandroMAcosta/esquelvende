from django.db.models import Q
import re


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    """
        Splits the query string in invidual keywords, getting
        rid of unecessary spaces and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  "spaces')
        ['some', 'random', 'words', 'with quotes', 'spaces']

    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, fields, filter_by):
    """
        Devuelve una query, esta es una combinacion de objetos Q.
        Esta combinacion sirve para filtrar un modelo probando los campos
        dados.
    """

    query = None
    if query_string and filter_by is None:
        terms = normalize_query(query_string)
        for term in terms:
            or_query = None
            for field in fields:
                q = Q(**{"%s__unaccent__icontains" % field: term}) |\
                    Q(**{"%s__unaccent__trigram_similar" % field: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
    elif query_string is None and filter_by:
        pass

    query = query & Q(active=True, delete=False)
    return query
