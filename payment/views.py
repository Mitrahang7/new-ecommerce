from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from store.models import Product,Category,Profile,OrderItem,Order
from django.contrib import messages
from cart.cart import Cart
from django.utils import timezone

@login_required
def biling_info(request):
  cart= Cart(request)
  cart_products= cart.get_prods
  quantities= cart.get_quants
  totals= cart.cart_total()

  profile, created = Profile.objects.get_or_create(user=request.user)
  

  if request.method == "POST":
        profile.phone = request.POST.get("phone", "")
        profile.address1 = request.POST.get("address1", "")
        profile.address2 = request.POST.get("address2", "")
        profile.disrtict = request.POST.get("city", "")  
        profile.province = request.POST.get("state", "") 
        profile.save()

        messages.success(request, "Your Info Has Been Updated!!")
        return redirect('checkout')
  return render(request, 'payment/biling_info.html', {'profile':profile, 'cart_products':cart_products,'quantities':quantities,'totals':totals})


@login_required
def checkout(request):
  cart= Cart(request)
  cart_products= cart.get_prods()
  quantities= cart.get_quants()
  totals= cart.cart_total()
  profile = Profile.objects.get(user=request.user)

  if request.method == "POST":
        if not cart_products:
            messages.error(request, "Your cart is empty!")
            return redirect('cart_page')

        order = Order.objects.create(user=request.user, total_price=totals)

        for product in cart_products:
          quantity = quantities.get(str(product.id), 1)
          OrderItem.objects.create(order=order, product=product, quantity=quantity)

       
        cart.clear()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

  return render(request, 'payment/checkout.html', {'profile':profile, 'cart_products':cart_products,'quantities':quantities,'totals':totals})

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(status='Completed')

        if request.method == "POST":
            order_id = request.POST.get('order_id')  

            order = Order.objects.filter(id=order_id).first() 
            if order is None:
                
                messages.error(request, "Order not found.")
                return redirect('shipped_dash')

            
            if order.status == 'Completed':
                order.status = 'Pending'
                order.shipped_at = None  
            elif order.status == 'Pending':
                order.status = 'Completed'
                order.shipped_at = timezone.now() 

            order.save()

            messages.success(request, f"Order status updated to {order.status}.")
            return redirect('shipped_dash')

        return render(request, 'payment/shipped_dash.html', {'orders': orders})

    else:
        messages.error(request, 'Access Denied')
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(status='Pending')

        if request.method == "POST":
            
            order_id = request.POST.get('order_id') 
            order = Order.objects.get(id=order_id)

            if order.status == 'Pending':
                order.status = 'Completed'
                order.shipped_at = timezone.now()  
            elif order.status == 'Completed':
                order.status = 'Pending'
                order.shipped_at = None 

            order.save()

            messages.success(request, f"Order status updated to {order.status}.")
            return redirect('not_shipped_dash')  
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})

    else:
        messages.error(request, 'Access Denied') 
        return redirect('home')

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.method == "POST":
            if order.status == 'Pending':
                order.status = 'Completed'
                order.shipped_at = timezone.now()
            elif order.status == 'Completed':
                order.status = 'Pending'
                order.shipped_at = None 
            order.save()

            messages.success(request, f"Order status updated to {order.status}.")
            return redirect('home')

        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, 'Access Denied')
        return redirect('home')
