
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from E_Commerse.models import Customer,AddToCart,ProductImage,ProductDetail,Order
#for file uploading
from django.core.files.storage import FileSystemStorage

#django payment
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import HttpResponseBadRequest
#for logout
from django.contrib.auth import logout

curl = settings.C_URL
media_url=settings.MEDIA_URL
# Create your views here.
def Logout(request):
    logout(request)
    return redirect('http://localhost:8000/login/')

def sessioncheckcustomer_middleware(get_response):
    def middleware(request):
        print("============= request=====:",request.path)
        strpath = request.path
        list1 = strpath.split("/")
        print(list1)
        if len(list1)>2:
            strnewpath = "/"+list1[1]+"/"+list1[2]+"/"
            if strnewpath=='/customer/home/' or strnewpath=='/customer/cart/' or strnewpath=='/customer/editprofile/' or strnewpath == '/customer/changepassword/' or strnewpath == '/changepassword/' or strnewpath == '/forgotpassword/' :
                if 'emailid' not in request.session:            
                    response=redirect('http://localhost:8000/login')
                else:
                    response=get_response(request)
            else:
                response=get_response(request)
        else:
            return get_response(request)        
        return response
        
    return middleware 



@csrf_exempt
def home(request):
    if request.method == "GET":
        #==============session
        emailid=request.session.get("emailid")
        password=request.session.get("password")
        #==============session 
        qs=Customer.objects.filter(email=emailid,password=password).values("name","email","mobile","address")
        # print(qs[0])
        #==========Product Details===============
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        # print("Product Images:",prod_img)
        prod_details=ProductDetail.objects.all().values("product_brand","product_description","product_price","product_id")
        # print(prod_details)
   
        prod_images=[]
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
    #=========================
        return render(request,'CustomerHome.html',{'curl':curl,'data':qs[0],'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})
    
    if request.method == "POST":
        result = request.POST.get('search')
        print("Search data:",result)
        prod_details=ProductDetail.objects.filter(product_brand=result).values()
        print(prod_details)
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        prod_images=[] 
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
        return render(request,'CustomerHome.html',{'curl':curl,'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})

def cart(request):
    if request.method == "GET":
         #==============session
        emailid=request.session.get("emailid")
        password=request.session.get("password")
        #==============session 
        cust_id=Customer.objects.filter(email=emailid,password=password).values("customer_id")
        print(cust_id[0])
        addtocart=AddToCart.objects.filter(customer_id=cust_id[0]["customer_id"]).values()
        print("Add to Cart:===========>",addtocart)
        sum=0
        for dic in addtocart:
            print(dic["product_total_price"])
            sum+=dic["product_total_price"]

        return render(request,'Cart.html',{'curl':curl,'addtocart':addtocart,'sum':sum,'media_url':media_url})

def productdetails(request):
    
    if request.method=="GET":
        product_id=request.GET.get('id')
        print("<=======product_id:========>",product_id)
        prod_img = ProductImage.objects.filter(product_id=product_id).values("product_img")
        print("Product Images:",prod_img)
        
        prod_details=ProductDetail.objects.filter(product_id=product_id).values()
        print(prod_details)
        product_size=prod_details[0]["product_size"]
        print("Product Size:",product_size)
        
        listofsize=product_size.split(",")

        redirecting='customer/cart/'

        return render(request,'DetailProduct.html',{'curl':curl,'prod_details':prod_details[0],'prod_images':prod_img,'redirecting':redirecting,'media_url':media_url,"product_id":product_id,'size':listofsize})
    

    elif request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(quantity,"=========")
        product_id=request.POST.get('product_id')
        product_img_id=request.POST.get('product_img_id')

        size=request.POST.get("size")
        print("<=======product_Size:========>",size)
        print("<=======product_id:========>",product_id)

        prod_img = ProductImage.objects.filter(product_id=int(product_id)).values("product_img","product_id")
        print("Product Images:",prod_img)
        
        prod_details=ProductDetail.objects.filter(product_id=int(product_id)).values()
        print(prod_details)
        product_quantity=prod_details[0]["product_quantity"]
        print("Product Quantity:",product_quantity)
        print("=======",prod_img[0]["product_img"])
        print("<=======product_img_id:========>",prod_img[0]["product_id"])

        single_img=prod_img[0]["product_img"]
        product_img_id=prod_img[0]["product_id"]
        product_brand=prod_details[0]["product_brand"]
        product_description=prod_details[0]["product_description"]
        #product_quantity=prod_details[0]["product_quantity"]
        product_price=prod_details[0]["product_price"]
        #=======================
        prod_detail = ProductDetail.objects.get(product_id=product_id)
        #===========session
        customer_id=request.session.get("customer_id")
        #=============
        cust_detail = Customer.objects.get(customer_id=customer_id)
        print("DataType====>",type(product_img_id))
        product_img_details = ProductImage.objects.filter(product_id_id=product_img_id).first()
        #================================
        product_total_price=int(quantity)*product_price
        print(product_total_price)
        print("=====customer cart=====")
        addtocart = AddToCart(product_img=single_img,product_brand=product_brand,product_size=size,product_description=product_description,product_quantity=int(quantity),product_price=product_price,product_total_price=product_total_price,product_id=prod_detail,customer_id=cust_detail,product_img_id=product_img_details)
        addtocart.save()
    return redirect(curl+"customer/cart/")

def customerdetails(request):
    #==============session
    emailid=request.session.get("emailid")
    password=request.session.get("password")
    #==============session 
    cust=Customer.objects.filter(email=emailid,password=password).values()
    print(cust)
    fullname=cust[0]["name"]
    list=fullname.split(" ")
    firstname=list[0]
    lastname=list[1]
    #==============session
    customer_id=request.session.get("customer_id")
    #==============session 
    cartdetails=AddToCart.objects.filter(customer_id=customer_id).values("product_total_price")

    print(cartdetails)

    return render(request,'CustomerDetails.html',{'curl':curl,"customer":cust[0],"firstname":firstname,"lastname":lastname,"total_price":cartdetails[0]["product_total_price"]})
    
def deleteproduct(request):
    if request.method=="GET":
        id=request.GET.get('id')
        print("Product Id:",id)
        AddToCart.objects.filter(product_id=id).delete()
        return redirect(curl+'customer/cart/') 
'''    
@csrf_exempt    
def payment(request):
    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    price=request.GET.get('price')
    currency = 'INR'
    amount = 5000
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount,currency=currency,payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = curl+'customer/paymenthandler/'

    print("============== Payment:",razorpay_order)
    listofdic=Customer.objects.filter(email="rahulsharma@gmail.com",password=12345).values()
    print(listofdic[0])
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['price']=price
    context['customer']=listofdic[0]
    
    return render(request, 'Payment1.html', context=context,)
''' 
     
  
@csrf_exempt
def payment(request):
    #==============session
    emailid=request.session.get("emailid")
    password=request.session.get("password")
    customer_id=request.session.get("customer_id")
    #==============session  
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])

    # authorize razorpay client with API Keys.
    client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" ,"payment_capture":'0'}
    # payment = client.order.create(data=data)
    print("============== Payment:",payment)
    price=request.GET.get('price')
    
    # Create a Razorpay Order
    razorpay_order = client.order.create(data=data)

    print(razorpay_order)
 
    #return render(request, 'index.html', context=context)
    return render(request,'Payment.html',{'price':price,'customer':listofdic[0],'curl':curl,"customer_id":customer_id})

    
def editprofile(request):
    if request.method == "GET":
        #==============session
        emailid=request.session.get("emailid")
        password=request.session.get("password")
        #==============session  
        cust=Customer.objects.filter(email=emailid,password=password).values()
        print(cust[0])
        return render(request,'CustomerEditProfile.html',{'curl':curl,'record':cust[0]})
    
    elif request.method == "POST":
        customer_id = request.POST.get('customer_id')
        name = request.POST.get('name')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        print(customer_id,name,mobile,address,city,pincode)
        Customer.objects.filter(customer_id=customer_id).update(name=name,city=city,pincode=pincode,address=address,mobile=mobile)
        msg="Record Updated Successfully"
        return render(request,'Message.html',{'curl':curl,'msg':msg})

def msg(request):
    return render(request,'Message.html',{'curl':curl})

def changepassword(request):
    if request.method == "GET":
        return render(request,'CustomerChangePassword.html',{"curl":curl})
    
    elif request.method == "POST":
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        print(oldpassword,newpassword,confirmpassword)
        #==============session
        emailid=request.session.get("emailid")
        #==============session  
        customer = Customer.objects.filter(email=emailid,password=oldpassword)
        print(customer)
        msg=""
        if customer.exists():
            print("==========Hiii")
            if newpassword==confirmpassword:
              #==============session
              emailid=request.session.get("emailid")
              #==============session  
              Customer.objects.filter(email=emailid,password=oldpassword).update(password=confirmpassword)
              msg="Customer Password Changed Successfully"  
            else:
              msg="New Password & Confirm Password are mismatch"
        else:
            print("============Hello")
            msg="Please enter correct old password!!"             
                
    return render(request,'CustomerChangePassword.html',{'curl':curl,'msg':msg})

@csrf_exempt
def paymentstatus(request):
    if request.method=="POST":
      #==============session
      customer_id=request.GET.get('id')
      print("customer_id aagai kya?",customer_id)
      #==============session  
      addtocart = AddToCart.objects.filter(customer_id_id=customer_id).values()
      print("===========addtocart:",addtocart)
      print(addtocart[0]["product_brand"])
      product_brand=addtocart[0]["product_brand"]
      product_price=addtocart[0]["product_price"]
      product_size=addtocart[0]["product_size"]
      product_description=addtocart[0]["product_description"]
      product_quantity=addtocart[0]["product_quantity"]
      product_img=addtocart[0]["product_img"]
      product_id=addtocart[0]["product_id_id"]
      customer_id=addtocart[0]["customer_id_id"]
      product_img_id=addtocart[0]["product_img_id_id"]
      print(product_brand,product_price,product_size,product_description,product_quantity,product_img,product_id,customer_id,product_img_id)

      #============
      cust_details = Customer.objects.get(customer_id=customer_id)
      prod_details = ProductDetail.objects.get(product_id=product_id)
      prod_img_details = ProductImage.objects.get(product_img_id=product_img_id)
      #===============

      #===Order
      order = Order(product_brand=product_brand,product_price=product_price,product_size=product_size,product_description=product_description,product_quantity=product_quantity,product_img=product_img,customer_id_id=customer_id,product_id_id=product_id,product_img_id_id=product_img_id)
      order.save()

      addtocart = AddToCart.objects.filter(customer_id_id=customer_id)
      addtocart.delete()
      return render(request,'PaymentSuccess.html',{'curl':curl})

def order(request):
    #==============session
    customer_id=request.session.get("customer_id")
    #==============session  
    order=Order.objects.filter(customer_id_id=customer_id).values()
    print(order)
    return render(request,'Orders.html',{'curl':curl,'order':order,'media_url':media_url})

def wishlist(request):
    return render(request,'WishList.html',{'curl':curl})
def Logout(request):
    logout(request)
    return redirect('http://localhost:8000/login/')



@csrf_exempt
def paymenthandler(request):
    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print("=========>",params_dict)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()