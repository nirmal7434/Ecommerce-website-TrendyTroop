from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.template.context_processors import request
from rest_framework import serializers
from clothe_app.models import Product,Category,Size,Review,ProductSize,Cart,Wishlist,Order,OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSizeSerializer(serializers.ModelSerializer):
    size_name = serializers.CharField(source='size.name', read_only=True)
    product_info = serializers.SerializerMethodField()
    class Meta:
        model = ProductSize
        fields = '__all__'

    def get_product_info(self,obj):
        return {
            "id":obj.product.id,
            "name":obj.product.name,
            "price":obj.product.price,
            "image":obj.product.image.url
        }


class ProductSerializer(serializers.ModelSerializer):
    product_sizes = ProductSizeSerializer(many=True,read_only=True)
    total_stock = serializers.SerializerMethodField()
    in_wishlist = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_total_stock(self,obj):
        total = obj.product_sizes.aggregate(total=Sum('stock'))['total']
        return total or 0

    def get_in_wishlist(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user,product=obj).exists()
        return False

class CartSerializer(serializers.ModelSerializer):
    product_size = ProductSizeSerializer(read_only=True)
    product_size_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductSize.objects.all(),
        write_only=True
    )
    line_total = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        product_size = validated_data.pop('product_size_id')
        cart = Cart.objects.create(product_size=product_size, **validated_data)
        return cart

    def get_line_total(self,obj):
        return obj.product_size.product.price * obj.quantity


class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError({"username":"username is required"})
        if not password:
            raise serializers.ValidationError({"password":"password is required"})

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"Invalid username"})

        if not user_obj.check_password(password):
            raise serializers.ValidationError({"password":"Incorrect password"})

        user = authenticate(request=self.context.get('request'),username=username,password=password)
        if user is None:
            raise serializers.ValidationError({"error":"Login failed"})

        data['user'] = user
        return data






