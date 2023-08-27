from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory
from .forms import AddProductForm, UpdateProductForm, RegistrationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django_pandas.io import read_frame
import difflib
import plotly
import plotly.express as px
import plotly.utils
import pandas as pd
import json
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Registered Account")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'inventory_system/register.html', {
        'title': 'Register',
        'form': form})



@login_required
def search_product(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'error': 'No query provided'})

    # Filter inventory for products created by the current active user
    results = Inventory.objects.filter(Q(name__iexact=query) & Q(user=request.user))
    if results.exists():
        first_result = results.first()
        return JsonResponse({'exact_match': True, 'redirect_pk': first_result.pk})

    suggested_product = None

    # If no exact match, check for similar names and suggest
    all_product_names = Inventory.objects.filter(Q(user=request.user)).values_list('name', flat=True)
    suggested_product_names = difflib.get_close_matches(query, all_product_names, n=1)
    if suggested_product_names:
        suggested_product_name = suggested_product_names[0]
        suggested_product_obj = Inventory.objects.filter(name=suggested_product_name).first()
        if suggested_product_obj and suggested_product_name.lower() != query.lower():
            suggested_product = {'name': suggested_product_name, 'pk': suggested_product_obj.pk}

    return JsonResponse({'exact_match': False, 'suggested_product': suggested_product})


@login_required
def inventory_list(request):
    user = request.user
    all_products = Inventory.objects.filter(user=user)

    if not all_products.exists():
        return redirect("empty_inventory")

    return render(request, "inventory/inventory_list.html", {
        "title": "Inventory List",
        "all_products": all_products,
    })

def empty_inventory(request):
    return render(request, "inventory/empty_inventory.html", {'title': 'Empty Inventory'})

@login_required
def per_product_view(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    return render(request, "inventory/per_product.html", {
        'title': 'Product Details',
        "product": product,
    })

@login_required
def add_product(request):
    if request.method == "POST":
        add_product_form = AddProductForm(data=request.POST)
        if add_product_form.is_valid():
            product_name = add_product_form.cleaned_data['name']

            # Check if a product with the same name already exists
            if Inventory.objects.filter(name__iexact=product_name, user=request.user).exists():
                messages.error(request, "Product name is already taken.")
            else:
                new_product = add_product_form.save(commit=False)
                new_product.user = request.user
                new_product.sales = float(add_product_form.cleaned_data['cost_per_item']) * float(add_product_form.cleaned_data['quantity_sold'])
                new_product.save()
                messages.success(request, "Successfully Added Product")
                return redirect("inventory_list")
    else:
        add_product_form = AddProductForm()

    return render(request, "inventory/inventory_add.html", {
        'title': 'Add New Product',
        "form": add_product_form})

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

    return render(request, "inventory/inventory_update.html", {
        'title': 'Update Product',
        "form": update_product_form})


def confirm_sale(request, product_id):
    if request.method == "POST":
        try:
            product = Inventory.objects.get(pk=product_id, user=request.user)

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
            product = Inventory.objects.get(pk=product_id, user=request.user)

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

@login_required
def dashboard(request):
    user = request.user
    all_products = Inventory.objects.filter(user=user)

    if not all_products.exists():
        return redirect("empty_inventory")

    df = read_frame(all_products)

    daily_product_sales_graph = create_daily_product_sales_graph(df)
    highest_sales_graph = create_highest_sales_graph(df)
    most_sold_products = create_most_sold_products_graph(df)
    most_product_in_stock = create_most_product_in_stock_graph(df)

    context = {
        'title': 'Dashboard',
        "daily_product_sales_graph": daily_product_sales_graph,
        "highest_sales_graph": highest_sales_graph,
        "most_sold_products": most_sold_products,
        "most_product_in_stock": most_product_in_stock
    }

    return render(request, "inventory/dashboard.html", context=context)

def create_daily_product_sales_graph(df):
    df['last_sales_date'] = pd.to_datetime(df['last_sales_date']).dt.date
    daily_product_sales_graph = px.bar(df,
                                      x='last_sales_date',
                                      y='sales',
                                      color='name',
                                      title="Daily Product Sales Distribution Graph")
    daily_product_sales_graph.update_xaxes(title_text="Sales Date")
    daily_product_sales_graph.update_yaxes(title_text="Sales")
    daily_product_sales_graph.update_layout(barmode='stack')
    daily_product_sales_graph.update_layout(title_x=0.5)
    daily_product_sales_graph = json.dumps(daily_product_sales_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return daily_product_sales_graph

def create_highest_sales_graph(df):
    highest_sales_products_df = df.groupby(by="name").sum().sort_values(by="sales", ascending=True)
    highest_sales_graph = px.bar(highest_sales_products_df,
                                 x=highest_sales_products_df.index,
                                 y='sales',
                                 title="Products Sales Graph",
                                 labels={"sales": "Total Sales"},
                                 height=400)
    highest_sales_graph.update_xaxes(title_text="Product", tickangle=-45)
    highest_sales_graph.update_yaxes(title_text="Sales")
    highest_sales_graph.update_layout(title_x=0.5)
    highest_sales_graph = json.dumps(highest_sales_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return highest_sales_graph

def create_most_sold_products_graph(df):
    most_sold_products_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    most_sold_products = px.bar(most_sold_products_df,
                                x=most_sold_products_df.index,
                                y='quantity_sold',
                                title="Quantity Sold Graph")
    most_sold_products.update_xaxes(title_text="Product", tickangle=-45)
    most_sold_products.update_yaxes(title_text="Quantity Sold")
    most_sold_products.update_layout(title_x=0.5)
    most_sold_products = json.dumps(most_sold_products, cls=plotly.utils.PlotlyJSONEncoder)
    return most_sold_products

def create_most_product_in_stock_graph(df):
    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df,
                                    names=most_product_in_stock_df.index,
                                    values='quantity_in_stock',
                                    title="Product In Stock Graph")
    most_product_in_stock.update_layout(title_x=0.5)
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)
    return most_product_in_stock
