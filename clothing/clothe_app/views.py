import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from clothe_app.models import Product,Category,Size,Review,ProductSize,Cart,Wishlist,Order,OrderItem,PromoCode
from django.core.mail import send_mail, EmailMessage

from rest_framework.generics import get_object_or_404, GenericAPIView, CreateAPIView

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import generate_invoice

from .serializers import ProductSerializer, CategorySerializer, SizeSerializer, ReviewSerializer, ProductSizeSerializer, \
    CartSerializer, WishListSerializer, OrderSerializer, OrderItemSerializer, RegisterSerializer, LoginSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]  # HTML render enable
    template_name = 'shop.html'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cat']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        categories = Category.objects.all()
        return Response({'products': serializer.data,'categories':categories})


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer

class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]  # HTML render enable
    template_name = 'shop-details.html'

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
    #     return obj

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response({'product':serializer.data})


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SizeListView(generics.ListAPIView):
    queryset =  Size.objects.all()
    serializer_class = SizeSerializer

class SizeCreateView(generics.CreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class SizeUpdateView(generics.UpdateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class SizeDeleteView(generics.DestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class SizeRetrieveView(generics.RetrieveAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ProductSizeListView(generics.ListAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class ProductSizeCreateView(generics.CreateAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class ProductSizeUpdateView(generics.UpdateAPIView):
    queryset =  ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class ProductSizeDeleteView(generics.DestroyAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class ProductSizeRetrieveView(generics.RetrieveAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer

class CartListView(generics.ListAPIView):
    queryset =  Cart.objects.all()
    serializer_class =  CartSerializer
    renderer_classes = [TemplateHTMLRenderer]  # HTML render enable
    template_name = 'shopping-cart.html'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cart_total = sum([item.product_size.product.price * item.quantity for item in queryset])

        discount = request.session.get('discount', 0)
        final_total = request.session.get('final_total', cart_total)
        promo_code = request.session.get('promo_code', None)

        context ={
            'cart_items': serializer.data,
            'cart_total': cart_total,
            'discount': discount,
            'final_total': final_total,
            'promo_code': promo_code,
        }
        return Response(context)




class CartCreateView(generics.CreateAPIView):
    serializer_class = CartSerializer



    def perform_create(self, serializer):
        user = self.request.user
        product_size = serializer.validated_data['product_size_id']
        quantity =  serializer.validated_data['quantity']
        cart_item = Cart.objects.filter(user=user,product_size=product_size).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
             serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return redirect('/cart')

def update_cart_quantity(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('/cart')



class ApplyPromoCodeAPIView(APIView):

    def post(self, request):
        code = request.POST.get('promo_code')
        user = request.user

        if not code:
            messages.error(request, 'Please enter a promo code.')
            return redirect('/cart')

        try:
            promo = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            messages.error(request, 'Invalid promo code.')
            return redirect('/cart')

        # Check expiry
        if promo.expire_date < timezone.now():
            messages.error(request, 'This promo code has expired.')
            return redirect('/cart')

        # Already used
        if promo.redeem_by == user:
            messages.error(request, 'You have already used this promo code.')
            return redirect('/cart')

        # Issued to someone else
        else:
            # Issued to someone else
            if promo.issue_to and promo.issue_to != user:
                messages.error(request, 'This promo code is not issued to you.')
                return redirect('/cart')

            # Get cart items
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                messages.error(request, 'Your cart is empty.')
                return redirect('/cart')

            # Total calculation
            cart_total = sum(item.product_size.product.price * item.quantity for item in cart_items)

            # Min amount check
            if cart_total < promo.min_amount:
                messages.error(request, 'Promo code not valid for this cart amount.')
                return redirect('/cart')

            # Calculate discount
            if promo.type == 'percentage':
                discount = (cart_total * promo.value) / 100
            else:
                discount = promo.value

            final_total = cart_total - discount

            # Save in session
            request.session['discount'] = float(discount)
            request.session['final_total'] = float(final_total)
            request.session['promo_code'] = code

            promo.redeem_by = user
            promo.save()

            messages.success(request, f"Promo code '{code}' applied successfully!")
            return redirect('/cart')

class CartUpdateView(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDeleteView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self,request,*args,**kwargs):
        cart_item = self.get_object()
        self.perform_destroy(cart_item)
        return redirect('/cart')

class CartRetrieveView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class WishListView(generics.ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wishlist.html'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response({'wishlist_items':serializer.data})

class WishListCreateView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer

class WishListUpdateView(generics.UpdateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer

class WishListDeleteView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer

class WishListRetrieveView(generics.RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer

class OrderListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer =self.get_serializer(queryset,many=True)
        cart_total = sum([item.product_size.product.price * item.quantity for item in queryset])

        discount = request.session.get('discount', 0)
        final_total = request.session.get('final_total', cart_total)
        promo_code = request.session.get('promo_code', None)

        context = {
            'cart_order' : serializer.data,
            'discount': discount,
            'final_total': final_total,
            'cart_total': cart_total

        }

        return Response(context)

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemLIstView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemUpdateView(generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemRetrieveView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class  = OrderItemSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer


    def post(self,request):
        serializer = self.get_serializer(data=request.data,context = {'request':request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request,user)
            messages.success(request,"login successfully")
            return redirect('/')
        else:
            context={
                'login_errors':serializer.errors,
                'open_login':True,
                'post_data':request.POST
            }
            return render(request,'base.html',context)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            messages.success(request, "Account created successfully!")
            return redirect('send_registration_email',email=user.email,username=user.username)
        else:
            context = {
                'register_errors': serializer.errors,
                'open_register': True,
                'post_data': request.data
            }
            return render(request, 'index.html', context)

def send_registration_email(request,email,username):
    subject ="welcome to our site"
    message =f"hello {username},\n\n thank you for registering on our website"
    from_email = "nnnnbera9090@gmail.com"
    send_mail(subject,message,from_email,[email])
    messages.success(request,"Registration email sent successfully")
    return redirect('/')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/')


def add_to_wishlist(request,product_id):
    if not request.user.is_authenticated:
        return redirect('/signin')

    product = Product.objects.get(id=product_id)

    Wishlist.objects.create(user=request.user,product=product)
    messages.success(request,"product added your wishlist")
    return redirect('/products')

def remove_to_wishlist(request,product_id):
    if not request.user.is_authenticated:
        return redirect('/signin')

    product = Product.objects.get(id=product_id)

    wishlist_item = Wishlist.objects.filter(user=request.user,product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request,'product remove from your wishlist')

    return redirect('/products')
@login_required
def order(request):
    if request.method == 'POST':
        user = request.user
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        cart_items = Cart.objects.filter(user=user)
        cart_total = sum([item.product_size.product.price * item.quantity for item in cart_items])
        discount = request.session.get('discount', 0)
        final_total = float(cart_total) - float(discount)




        if payment_method == 'COD':
            order = Order.objects.create(
                user=user,
                fname=fname,
                lname=lname,
                email=email,
                address=address,
                phone=phone,
                total_amount=final_total,
                payment_method=payment_method,
                payment_status='Pending'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_size=item.product_size,
                    quantity=item.quantity,
                    price=item.product_size.product.price
                )
                item.product_size.stock -= item.quantity
                item.product_size.save()

            cart_items.delete()
            for key in ['discount', 'final_total', 'promo_code']:
                if key in request.session:
                    del request.session[key]
            pdf_buffer = generate_invoice(order)
            email_msg = EmailMessage(
                "Your Order Invoice",
                "Thank you for your order! Please find attached your invoice.",
                "nnnnbera9090@gmail.com",
                [email],
            )
            email_msg.attach(f"Invoice_Order_{order.id}.pdf", pdf_buffer.getvalue(), "application/pdf")
            email_msg.send()
            return redirect('/')
        elif payment_method == 'Razorpay':
            if final_total < 1:
                messages.error(request, "Order amount Razorpay માટે ખૂબ ઓછું છે.")
                return redirect('/cart')
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

            payment_data = {
                "amount": int(final_total * 100),
                "currency": "INR",
                "payment_capture": "1",
            }

            order_data = client.order.create(data=payment_data)

            new_order = Order.objects.create(
                user=request.user,
                fname=fname,
                lname=lname,
                email=email,
                address=address,
                phone=phone,
                total_amount=final_total,
                payment_status="Pending",
                payment_method="Razorpay",
                razorpay_order_id=order_data["id"]
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=new_order,
                    product_size=item.product_size,
                    quantity=item.quantity,
                    price=item.product_size.product.price
                )
                item.product_size.stock -= item.quantity
                item.product_size.save()
            cart_items.delete()

            context = {
                "order": new_order,
                "cart_order": cart_items,
                "cart_total": cart_total,
                "discount": discount,
                "final_total": final_total,
                "razorpay_order_id": order_data["id"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount_in_paise": int(final_total * 100),
                "total": final_total,
            }

            return render(request, "checkout.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
        if order:
            order.payment_status = "Confirmed"
            order.save()

            pdf_buffer = generate_invoice(order)
            email_msg = EmailMessage(
                "Your Order Invoice (Payment Confirmed)",
                "Thank you for your payment! Please find attached your invoice.",
                "nnnnbera9090@gmail.com",
                [order.email],
            )
            email_msg.attach(f"Invoice_Order_{order.id}.pdf", pdf_buffer.getvalue(), "application/pdf")
            email_msg.send()

    messages.success(request, "Payment successful! Your order has been confirmed.")
    return redirect('/orders')



@login_required
def orders(request):
    order_items = Order.objects.filter(user=request.user).order_by('-id')
    return render(request,'orderlist.html',{'order_items':order_items})




def wishlist(request):
    return render(request,'wishlist.html')
def home(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def blog(request):
    return render(request,'blog.html')
def blogdetails(request):
    return render(request,'blog-details.html')
def contact(request):
    return render(request,'contact.html')
def main(request):
    return render(request,'main.html')
# def shop(request):
#     return render(request,'shop.html')
def shopdetails(request):
    return render(request,'shop-details.html')
# def cart(request):
#     return render(request,'shopping-cart.html')
# def orders(request):
#     return render(request,'orderlist.html')
# def checkout(request):
#     return render(request,'checkout.html')




