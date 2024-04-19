import django_filters 

from .models import Comment


class CommentFilter(django_filters.FilterSet):
    article = django_filters.CharFilter()
    author = django_filters.CharFilter(method='author_filter')
    sort = django_filters.OrderingFilter(fields=('article', 'author', 'created', 'updated', 'is_great'))

    def author_filter(self, queryset, field_name, value):
        return queryset.filter(author__username__icontains=value)