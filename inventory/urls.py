from django.urls import path

from . import views


urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("empty_inventory/", views.empty_inventory, name="empty_inventory"),
    path("search_product/", views.search_product, name="search_product"),
    path("per_product/<int:pk>", views.per_product_view, name="per_product"),
    path("add_inventory/", views.add_product, name="add_inventory"),
    path("delete/<int:pk>", views.delete_inventory, name="delete_inventory"),
    path("update/<int:pk>", views.update_inventory, name="update_inventory"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("confirm_sale/<int:product_id>", views.confirm_sale, name="confirm_sale"),
    path("confirm_stock/<int:product_id>", views.confirm_stock, name="confirm_stock"),
]
