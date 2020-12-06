from rest_framework import serializers
from HelloDjango.models import Category, Pricelist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
                    'password': {
                        'write_only': True,
                    }
                }
        
    def create(self, validated_data):
            obj = User.objects.create(**validated_data)
            return obj

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.last_login = validated_data.get('last_login', instance.last_login)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.save()
        return instance

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('pk', UserModel.USERNAME_FIELD, UserModel.EMAIL_FIELD, 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('email', )


class PricelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricelist
        fields = '__all__'

        extra_kwargs = {}

    def create(self, validated_data):
        obj = Pricelist.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.option = validated_data.get('option', instance.option)
        instance.price = validated_data.get('price', instance.price)
        instance.count = validated_data.get('count', instance.count)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
        
class CategorySerializer(serializers.ModelSerializer):
    categories = PricelistSerializer(source='pricelists', many=True, required=False)
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = { 
        }

    def create(self, validated_data):
        obj = Category.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.section = validated_data.get('section', instance.section)
        instance.name = validated_data.get('name', instance.name)
        instance.producer = validated_data.get('producer', instance.producer)
        instance.flavor = validated_data.get('flavor', instance.flavor)
        instance.age = validated_data.get('age', instance.age)
        instance.description = validated_data.get('description', instance.description)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance


class FilterSerializer(serializers.Serializer):
    producer = serializers.ListField()
    maxPrice = serializers.FloatField()
    minPrice = serializers.FloatField()