from .models import Category

def get_categories(request):
    query = Category.objects.all()
    return {'categories': query}
