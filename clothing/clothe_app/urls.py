from django.urls import path, include

from . import views
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CategoryRetrieveView, \
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductRetrieveView, SizeListView, \
    SizeCreateView, SizeUpdateView, SizeDeleteView, SizeRetrieveView, ReviewListView, ReviewCreateView, \
    ReviewUpdateView, ReviewDeleteView, ReviewRetrieveView, ProductSizeListView, ProductSizeCreateView, \
    ProductSizeUpdateView, ProductSizeDeleteView, ProductSizeRetrieveView, CartListView, CartCreateView, CartUpdateView, \
    CartDeleteView, CartRetrieveView, WishListView, WishListCreateView, WishListUpdateView, WishListDeleteView, \
    WishListRetrieveView, OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderRetrieveView, \
    OrderItemLIstView, OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView, OrderItemRetrieveView, \
    RegisterView, LoginView, send_registration_email

urlpatterns = [
    # path('category/',CategoryListView.as_view(),name='category-list'),
    # path('category/add/',CategoryCreateView.as_view(),name='category-create'),
    # path('category/<int:pk>/edit/',CategoryUpdateView.as_view(),name='category-update'),
    # path('category/<int:pk>/delete/',CategoryDeleteView.as_view(),name='category-delete'),
    # path('category/<int:pk>/',CategoryRetrieveView.as_view(),name='category-detail'),
    path('category/', include([
        path('', CategoryListView.as_view(),name='category-list'),
        path('add/', CategoryCreateView.as_view(),name='category-create'),
        path('<int:pk>/edit/', CategoryUpdateView.as_view(),name='category-update'),
        path('<int:pk>/delete/', CategoryDeleteView.as_view(),name='category-delete'),
        path('<int:pk>/', CategoryRetrieveView.as_view(),name='category-detail'),
    ])),
    path('products/',ProductListView.as_view(),name='product-list'),
    path('products/add/',ProductCreateView.as_view(),name='product-create'),
    path('products/<int:pk>/edit/',ProductUpdateView.as_view(),name='product-update'),
    path('products/<int:pk>/delete/',ProductDeleteView.as_view(),name='product-delete'),
    path('products/<int:pk>/',ProductRetrieveView.as_view(),name='product-detail'),
    path('size/',SizeListView.as_view(),name='size-list'),
    path('size/add/',SizeCreateView.as_view(),name='size-create'),
    path('size/<int:pk>/edit/',SizeUpdateView.as_view(),name='size-update'),
    path('size/<int:pk>/delete/',SizeDeleteView.as_view(),name='size-delete'),
    path('size/<int:pk>/',SizeRetrieveView.as_view(),name='size-detail'),
    path('review/',ReviewListView.as_view(),name='review-list'),
    path('review/add/',ReviewCreateView.as_view(),name='review-create'),
    path('review/<int:pk>/edit/',ReviewUpdateView.as_view(),name='review-update'),
    path('review/<int:pk>/delete/',ReviewDeleteView.as_view(),name='review-delete'),
    path('review/<int:pk>/',ReviewRetrieveView.as_view(),name='review-detail'),
    path('productsize/',ProductSizeListView.as_view(),name='productsize-list'),
    path('productsize/add/',ProductSizeCreateView.as_view(),name='productsize-create'),
    path('productsize/<int:pk>/edit/',ProductSizeUpdateView.as_view(),name='productsize-update'),
    path('productsize/<int:pk>/delete/',ProductSizeDeleteView.as_view(),name='productsize-delete'),
    path('productsize/<int:pk>/',ProductSizeRetrieveView.as_view(),name='productsize-detail'),
    path('cart/',CartListView.as_view(),name='cart-list'),
    path('cart/<int:pk>/add/',CartCreateView.as_view(),name='cart-create'),
    path('cart/<int:pk>/edit/',CartUpdateView.as_view(),name='cart-update'),
    path('cart/<int:pk>/delete/',CartDeleteView.as_view(),name='remove_from_cart'),
    path('cart/<int:pk>/',CartRetrieveView.as_view(),name='cart-detail'),
    path('wishlist/',WishListView.as_view(),name='wishlist-list'),
    # path('wishlist/add/',WishListCreateView.as_view(),name='wishlist-create'),
    # path('wishlist/<int:pk>/edit/',WishListUpdateView.as_view(),name='wishlist-update'),
    # path('wishlist/<int:pk>/delete/',WishListDeleteView.as_view(),name='wishlist-delete'),
    # path('wishlist/<int:pk>/',WishListRetrieveView.as_view(),name='wishlist-detail'),
    path('order/',OrderListView.as_view(),name='order-list'),
    path('order/add/',OrderCreateView.as_view(),name='order-create'),
    path('order/<int:pk>/edit/',OrderUpdateView.as_view(),name='order-update'),
    path('order/<int:pk>/delete/',OrderDeleteView.as_view(),name='order-delete'),
    path('order/<int:pk>/',OrderRetrieveView.as_view(),name='order-detail'),
    path('orderitem/',OrderItemLIstView.as_view(),name='orderitem-list'),
    path('orderitem/add/',OrderItemCreateView.as_view(),name='orderitem-create'),
    path('orderitem/<int:pk>/edit/',OrderItemUpdateView.as_view(),name='orderitem-update'),
    path('orderitem/<int:pk>/delete/',OrderItemDeleteView.as_view(),name='orderitem-delete'),
    path('orderitem/<int:pk>/',OrderItemRetrieveView.as_view(),name='orderitem-detail'),
    # path('signup', views.signup, name="signup"),
    path('signup',RegisterView.as_view(),name='register'),
    # path('signin',views.signin,name="signin"),
    path('signin',LoginView.as_view(),name='signin'),
    path('signout',views.signout,name="signout"),
    path('wishlist/add/<int:product_id>/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',views.remove_to_wishlist,name='remove_to_wishlist'),
    path('', views.home, name='home'),
    path('about/', views.about),
    path('blog/', views.blog),
    path('contact/', views.contact),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('blogdetails/',views.blogdetails),
    # path('checkout/',views.checkout),
    path('main/',views.main),
    # path('shop/',views.shop),
    # path('shoppingcart/', views.cart),
    path('place_order/', views.order,name='place_order'),
    path('shopdetail/', views.shopdetails),
    path('cart/<int:cart_id>/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('apply-promo/',views.apply_promo_code,name='apply_promo_code'),
    path('order-detail/',views.orders,name='order-detail'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('send_registration_email/<str:email>/<str:username>/',send_registration_email,name='send_registration_email')

]