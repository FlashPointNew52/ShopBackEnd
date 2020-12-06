from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CategorySerializer, PricelistSerializer, UserSerializer
from .models import Category, Pricelist
from django.contrib.auth.models import User
from django.http import QueryDict


class UserApi(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return UserSerializer.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = UserSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        staff = request.GET.get("staff")
        if staff != None:
            objs = User.objects.filter(is_staff=staff)
        else:
            objs = User.objects.all()
        serializer = PricelistSerializer(objs, many=True)
        return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryApi(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def checkPicture(self, request):
        data = QueryDict.copy(request.data)
        if isinstance(data.get("picture"), str):
            if data.get("picture") == 'null':
                data.update({'picture': None})
            else: 
                data.pop("picture")
        return data    
        
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        data = self.checkPicture(request)
        serializer = CategorySerializer(category, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        data = self.checkPicture(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        section = request.GET.get("section")
        subsection = request.GET.get("subsection")
        if subsection != None and subsection != 'all':
            categories = Category.objects.filter(section=section, subsection=subsection)
        elif section != None and section != 'all':
            categories = Category.objects.filter(section=section)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class PricelistApi(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Pricelist.objects.get(pk=pk)
        except Pricelist.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = PricelistSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = PricelistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        category = request.GET.get("category")
        if category != None:
            categories = Pricelist.objects.filter(category_id=category)
        else:
            categories = Pricelist.objects.all()
        serializer = PricelistSerializer(categories, many=True)
        return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
