from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm, UpdateProductForm
from django.contrib import messages
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json
from django.http import JsonResponse

# Create your views here.
@login_required
def inventory_list(request):
    all_products = Inventory.objects.all()
    return render(request, "inventory/inventory_list.html", {
        "title": "Inventory List",
        "all_products": all_products,
    })

@login_required
def per_product_view(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    return render(request, "inventory/per_product.html", {
        "product": product
    })

@login_required
def add_product(request):
    if request.method == "POST":
        add_product_form = AddProductForm(data=request.POST)
        if add_product_form.is_valid():
            new_product = add_product_form.save(commit=False)
            new_product.sales = float(add_product_form.data['cost_per_item']) * float(add_product_form.data['quantity_sold'])
            new_product.save()
            messages.success(request, "Successfully Added Product")
            return redirect("/inventory/")
    else:
        add_product_form = AddProductForm()

    return render(request, "inventory/inventory_add.html", {"form": add_product_form})

@login_required
def delete_inventory(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    product.delete()
    messages.success(request, "Successfully Deleted Product")

    return redirect("/inventory/")

@login_required
def update_inventory(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        update_product_form = UpdateProductForm(data=request.POST)
        if update_product_form.is_valid():
            product.name = update_product_form.data['name']
            product.quantity_in_stock = update_product_form.data['quantity_in_stock']
            product.quantity_sold = update_product_form.data['quantity_sold']
            product.cost_per_item = update_product_form.data['cost_per_item']
            product.sales = float(product.cost_per_item) * float(product.quantity_sold)
            product.save()
            messages.success(request, "Successfully Updated Product")
            return redirect(f"/inventory/per_product/{pk}")

    else:
        update_product_form = UpdateProductForm(instance=product)

    return render(request, "inventory/inventory_update.html", {"form": update_product_form})

@login_required
def dashboard(request):
    all_products = Inventory.objects.all()

    df = read_frame(all_products)

    graph_of_sales = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    graph_of_sales = px.line(graph_of_sales, x = graph_of_sales.last_sales_date, y = graph_of_sales.sales, title="Sales Trend")
    graph_of_sales = json.dumps(graph_of_sales, cls=plotly.utils.PlotlyJSONEncoder)

    most_sold_products_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    most_sold_products = px.bar(most_sold_products_df,
                                    x = most_sold_products_df.index,
                                    y = most_sold_products_df.quantity_sold,
                                    title = "Best Performing Product"
                                     )
    most_sold_products = json.dumps(most_sold_products, cls=plotly.utils.PlotlyJSONEncoder)

    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df,
                                    names = most_product_in_stock_df.index,
                                    values = most_product_in_stock_df.quantity_sold,
                                    title = "Most Product In Stock"
                                     )
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": graph_of_sales,
        "best_performing_product": most_sold_products,
        "most_product_in_stock": most_product_in_stock
    }

    return render(request, "inventory/dashboard.html", context=context)


def confirm_sale(request, product_id):
    if request.method == "POST":
        try:
            product = Inventory.objects.get(pk=product_id)

            # Get the JSON data from the request body
            data = json.loads(request.body)
            sale_quantity = int(data.get("sale_quantity", 0))

            if sale_quantity >= 0 and product.quantity_in_stock >= sale_quantity:
                # Update the inventory values
                product.quantity_sold += sale_quantity
                product.sales += product.cost_per_item * sale_quantity
                product.quantity_in_stock -= sale_quantity

                # Save the changes
                product.save()

                # Prepare the response data
                response_data = {
                    "success": True,
                    "quantity_sold": product.quantity_sold,
                    "sales": product.sales,
                    "quantity_in_stock": product.quantity_in_stock,
                }
            else:
                response_data = {"success": False, "message": "Invalid sale quantity"}
        except Inventory.DoesNotExist:
            response_data = {"success": False, "message": "Product not found"}

        return JsonResponse(response_data)



def confirm_stock(request, product_id):
    if request.method == "POST":
        try:
            product = Inventory.objects.get(pk=product_id)

            # Get the JSON data from the request body
            data = json.loads(request.body)
            add_stock_quantity = int(data.get("add_stock_quantity", 0))

            if add_stock_quantity >= 0:
                # Update the inventory values
                product.quantity_in_stock += add_stock_quantity

                # Save the changes
                product.save()

                # Prepare the response data
                response_data = {
                    "success": True,
                    "updated_quantity_in_stock": product.quantity_in_stock,
                }
            else:
                response_data = {"success": False, "message": "Invalid stock quantity"}
        except Inventory.DoesNotExist:
            response_data = {"success": False, "message": "Product not found"}

        return JsonResponse(response_data)