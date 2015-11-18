
for e in OrderConfirmation.objects.filter(id=confirmation.id):
    confirmat = e.Confirmation
    tru = True
if confirmat == tru:
    user_num = len(User.objects.order_by('username'))
    WhoUser=request.user
    product_list = []
    price_list = []
    numproduct_list = []
    for e in Product.objects.filter(orderproductline__OrderID__orderconfirmation__id=confirmation.id):
        product_list.append(e.NameProduct)
        price_list.append(e.Price)
    product_list = [str(x) for x in product_list]
    k=0
    for i in product_list:
        for e in OrderProductLine.objects.filter(OrderID__orderconfirmation__id=confirmation.id, ProductID__NameProduct=product_list[k]):
            numproduct_list.append(e.NumProduct)
        k=k+1
    k=0                 
    user_balance = 0
    for i in product_list:
        user_balance = user_balance + price_list[k]*numproduct_list[k]
        k=k+1
    #_____________this user CashMove__________________    
    cashmove = CashMove(AmountMoney=user_balance, DateCashMove=timezone.now(), UserCash=request.user.userprofile )           
    cashmove.save() 
    #________________________________________
    
    #_____________others users CashMove_______________
    user_list = []
    for e in User.objects.exclude(username=WhoUser):
        user_list.append(e.username)
        
    user_list_id = []
    for e in User.objects.exclude(username=WhoUser):
        user_list_id.append(e.id)   
    
    user_list = [str(x) for x in user_list]
    new_balance = (-1)*user_balance/user_num
    
    k=0
    for i in user_list:
        cashmove = CashMove(AmountMoney=new_balance, DateCashMove=timezone.now(), UserCash_id=user_list_id[k] )
        cashmove.save()
        k=k+1                 
    #__________________________________________
    
    #_____________this user balance____________
    for e in UserProfile.objects.filter(user__username=WhoUser):
        this_balance = e.balance
     
    for e in CashMove.objects.filter(UserCash__user__username=WhoUser):
        this_cashmove = e.AmountMoney                
    
    new_user_balance = this_balance + this_cashmove
    
    Balance = UserProfile.objects.get(user__username=WhoUser)
    Balance.balance = new_user_balance
    Balance.save()
    #__________________________________________

    #_____________others user balance____________                
    user_list = []
    for e in User.objects.exclude(username=WhoUser):
        user_list.append(e.username)
        
    user_list = [str(x) for x in user_list]
    new_balance = (-1)*user_balance/user_num
    
    k=0
    for i in user_list:
        Balance = UserProfile.objects.get(user__username=user_list[k])
        Balance.balance = new_balance
        Balance.save()
        k=k+1            