from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Category, Pricelist
from .pagination import PaginationClass
from .serializers import CategorySerializer, PricelistSerializer, FilterSerializer
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Max, Min

class CategoryApi(GenericAPIView):
    parser_classes = [JSONParser]
    permission_classes = []
    pagination_class = PaginationClass
    
    def get(self, request, sec=None, subs=None, slug=None, format=None):
        if slug != None:
            obj = Category.objects.get(slug=slug)
            serializer = CategorySerializer(obj)
            return Response(serializer.data)
        else:
            sort = "minPrice"
            page = 1
            if request.GET.get("page"):
                page = int(request.GET.get("page"))
            if request.GET.get("limit"):
                limit = int(request.GET.get("limit"))
            if request.GET.get("sort"):
                sort = request.GET.get("sort")
            
            filters = {}
            
            for key, value in request.GET.items():
                if key in ['minPrice']:
                    filters.update({key+"__gte":value})
                if key in ['maxPrice']:
                    filters.update({key+"__lte":value})
                if key in ['producer', 'flavor', 'age']:
                    filters.update({key+"__in":request.GET.get(key).split(",")})
               
            if sec != None:
                filters.update({'section':sec})
            if subs != None:
                filters.update({'subsection':subs})
            paginator = PaginationClass()
            
            categories = Category.objects.filter(**filters).order_by(sort)
            
            pages = paginator.paginate_queryset(queryset=categories, request=request)
            categories = paginator.page.paginator.page(page)
            if page is not None:
                serializer = CategorySerializer(categories, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response("No page found", status=status.Http404)


class FilterApi(APIView):
    parser_classes = [JSONParser]
    permission_classes = []

    def get(self, request, sec=None, subs=None, format=None):
        filters = {}
        if sec != None and subs != None:
            categories = Category.objects.filter(section=sec, subsection=subs)
        elif sec != None and subs == None:
            categories = Category.objects.filter(section=sec)
        else:
            categories = Category.objects.all()
        
        ret = categories.values("producer").distinct()
        filters.update({"producer": categories.order_by("producer").values_list("producer", flat=True).distinct()})
        maxMin = categories.aggregate(Max('maxPrice'), Min('minPrice'))
        filters.update({"maxPrice": maxMin.get("maxPrice__max")})
        filters.update({"minPrice": maxMin.get("minPrice__min")})
        serializer = FilterSerializer(filters)
        return Response(serializer.data)
