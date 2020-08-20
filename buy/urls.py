from django.urls import path
from . import views

app_name = 'buy'

urlpatterns = [
    # here name is name of the url
    path('',views.allProdCat, name = 'allProdCat'), # just all products
    path('<slug:c_slug>/',views.allProdCat, name = 'products_by_category'), # products will all categories
    path('<slug:c_slug>/<slug:p_slug>/',views.allProducts,name = 'each_product_details'),#
]
