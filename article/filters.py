import django_filters 

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(method='tags_filter')
    author = django_filters.CharFilter(method='author_filter')
    # limit = django_filters.NumberFilter(method='limit_filter')
    # offset = django_filters.NumberFilter(method='offset_filter')
    sort = django_filters.OrderingFilter(fields=('views', 'author', 'created', 'updated'))
    
    class Meta:
        model = Article
        fields = ['tags', 'author', 'title', 'content']
     
    # def tags_filter(self, queryset, field_name, value):
    #     return queryset.filter(tags__name__in=[value])
    def tags_filter(self, queryset, name, value):
        if value == "ALL" or value == '':
            return queryset
        else:
            value_list = value.split(",")
            target_value_list = []
            for v in value_list:
                target_value_list.append(v.strip())
            return queryset.filter(tags__name__in=target_value_list)
    
    def author_filter(self, queryset, field_name, value):
        return queryset.filter(author__username__icontains=value)
 
    
    # # Limit number of articles (default is 20):
    # def limit_filter(self, queryset, field_name, value):
    #     return queryset[:value]
    
    # # Offset/skip number of articles (default is 0):
    # def offset_filter(self, queryset, field_name, value):
    #     return queryset[value:]