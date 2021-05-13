from app.models import *
import uuid
from rest_framework.response import Response
import datetime
import requests

def get_internal_error():
	data={'msg':'Internal Error'}
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def success_response(data):
	dic={'status':True, 'status_code':1000, 'data':data}
	return Response(dic)

def failure_response(data):
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def get_auth_token_error():
	data={'msg':'Incorrect Authorization Token'}
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def get_userid_Authorization(userid):
	Authorization=str(uuid.uuid5(uuid.NAMESPACE_DNS, userid))
	return Authorization

def check_Authorization(Authorization):
	users=UserData.objects.all()
	for x in users:
		if get_userid_Authorization(x.user_id) == Authorization:
			return True

def get_user_id_from_Authorization(Authorization):
	users=UserData.objects.all()
	for x in users:
		if get_userid_Authorization(x.user_id) == Authorization:
			return x.user_id

def get_batch_data(medicine_id):
	dic={}
	lt=[]
	for x in MedicineBatchData.objects.filter(medicine_id=medicine_id, status='1'):
		dic={
		'entry_date':x.created_date,
		'batch_id':x.batch_id,
		'batch_number':x.batch_number,
		'quantity':x.quantity,
		'expiry_date':x.expiry_date
		}
		lt.append(dic)
	return lt

def get_total_medicine_quatity(medicine_id):
	total=0
	for x in MedicineBatchData.objects.filter(medicine_id=medicine_id):
		total=total+float(x.quantity)
	return total

def get_medicines(ids):
	dic={}
	lt=[]
	for elt in ids:
		medicine_data=MedicineData.objects.filter(medicine_id=elt)[0]
		dic={
			'id':str(medicine_data.medicine_id),
			'name':str(medicine_data.medicine_name),
			'mesuring_unit':str(medicine_data.medicine_measuringunit),
			'1_strip_equals':str(medicine_data.medicine_1stripequals),
			'cost_price':str(medicine_data.medicine_costprice),
			'sell_price':str(medicine_data.medicine_sellprice),
			'mrp':str(medicine_data.medicine_mrp),
			'fix_rate':str(medicine_data.medicine_fixedrate),
			'discount':str(medicine_data.medicine_discount),
			'gst':str(medicine_data.medicine_gst),
			'image':str(MedicineImageData.objects.filter(medicine_id=medicine_data.medicine_id)[0].medicine_image.url)
		}
		batches = []
		batch_dic = {}
		for batch in MedicineBatchData.objects.filter(medicine_id=elt, status='1'):
			batch_dic = {
				'batch_number':batch.batch_number,
				'batch_quantity':batch.quantity,
				'batch_expiry_date':batch.expiry_date
			}
			batches.append(batch_dic)
		dic.update({'batches':batches})
		lt.append(dic)
	return lt

def get_suggestions_id(store_id, keyword):
	medicines=MedicineData.objects.filter(store_id=store_id, status='1')
	medicine_ids=[]
	for medicine in medicines:
		keyword_2=''
		for key in str(medicine.medicine_name):
			keyword_2=keyword_2+str(key)
			if keyword.upper()==keyword_2.upper():
				medicine_ids.append(medicine.medicine_id)
	return get_medicines(medicine_ids)

def get_customer_suggestions_id(store_id, keyword):
	customers=StoreCustomerData.objects.filter(store_id=store_id)
	cus_lt=[]
	for cus in customers:
		keyword_2=''
		for key in str(cus.customer_name):
			keyword_2=keyword_2+str(key)
			if keyword.upper()==keyword_2.upper():
				dic={
				'customer_name':cus.customer_name,
				'customer_mobile':cus.customer_mobile,
				'customer_address':cus.customer_address,
				'customer_doctor':cus.customer_doctor
				}
				cus_lt.append(dic)
	return cus_lt

def get_tablet_price(medicine_id):
	medicine_data=MedicineData.objects.filter(medicine_id=medicine_id)[0]
	one_stripe_equals=float(medicine_data.medicine_1stripequals)
	tablet_price=float(medicine_data.medicine_mrp)/one_stripe_equals
	return tablet_price

def create_cart_id(store_id):
	c="CRT00"
	x=1
	cic=c+str(x)
	while CartData.objects.filter(cart_id=cic).exists():
		x=x+1
		cic=c+str(x)
	x=int(x)
	CartData(cart_id=cic, store_id=store_id).save()
	return cic

def create_bill_id(store_id):
	c="BILL00"
	x=1
	cic=c+str(x)
	while BillData.objects.filter(bill_id=cic).exists():
		x=x+1
		cic=c+str(x)
	x=int(x)
	return cic

def get_user_data(user_id):
	user_data={}
	for x in UserData.objects.filter(user_id=user_id, status='1'):
		user_data={
			'created_date':x.created_date,
			'user_id':x.user_id,
			'store_id':x.store_id,
			'user_email':x.user_email,
			'user_mobile':x.user_mobile,
			'user_name':x.user_name
		}
	return user_data

def get_number_of_low_stocks(store_id):
	count=0
	medicines=[]
	for x in MedicineData.objects.filter(store_id=store_id):
		if x.medicine_quantity == None or x.medicine_quantity == '' or x.medicine_quantity == 'Not Availi':
			count=count+1
			medicines.append(x.medicine_id)
		elif float(x.medicine_quantity) < 50:
			count=count+1
			medicines.append(x.medicine_id)
	return {'low_stocks_count':count, 'low_stocks_medicines':medicines}

def get_number_of_expired_stocks(store_id):
	count=len(MedicineData.objects.filter(store_id=store_id, contains_expired_stock='1'))
	medicines=[]
	for x in MedicineData.objects.filter(store_id=store_id, contains_expired_stock='1'):
		medicines.append(x.medicine_id)
	return {'expired_stocks_count':count, 'expired_stocks_medicines':medicines}

def get_today_revenue(store_id):
	today_date=datetime.date.today()
	bills=BillData.objects.filter(store_id=store_id, bill_date=today_date)
	total_revenue=0.0
	for x in bills:
		total_revenue=total_revenue+float(x.total_amount_to_pay)
	return total_revenue

def get_total_revenue(store_id):
	bills=BillData.objects.filter(store_id=store_id)
	total_revenue=0.0
	for x in bills:
		total_revenue=total_revenue+float(x.total_amount_to_pay)
	return total_revenue

def get_total_stocks_value(store_id):
	total=0.0
	for x in MedicineData.objects.filter(store_id=store_id):
		total=total+float(x.medicine_mrp)
	return total

def get_complete_transaction_data(store_id):
	data={}
	bills_list=[]
	for  x in BillData.objects.filter(store_id=store_id):
		data={
			'bill_id':x.bill_id,
			'bill_date':x.bill_date,
			'total_amount':x.total_amount_to_pay,
			'customer_name':StoreCustomerData.objects.filter(customer_id=x.customer_id)[0].customer_name
		}
		bills_list.append(data)
	return bills_list

def get_incomplete_transaction_data(store_id):
	data={}
	bills_list=[]
	for  x in CartData.objects.filter(store_id=store_id):
		data={
			'bill_id':x.cart_id,
			'bill_date':x.cart_date,
			'total_amount':x.total_amount_to_pay,
			'customer_name':StoreCustomerData.objects.filter(customer_id=x.customer_id)[0].customer_name
		}
		bills_list.append(data)
	return bills_list

def get_distributer_data(dist_id):
	dist=DistributerData.objects.filter(dist_id=dist_id)[0]
	data={
		'dist_id':dist.dist_id,
		'store_id':dist.store_id,
		'dist_name':dist.dist_name,
		'dist_email':dist.dist_email,
		'dist_mobile':dist.dist_mobile,
		'dist_address':dist.dist_address,
		'dist_gstin':dist.dist_gstin,
		'dist_balance':dist.dist_balance
	}
	return data

def get_medicine_info(medicine_id):
	medicine=MedicineData.objects.filter(medicine_id=medicine_id, status='1')[0]
	data={
		'created_date':str(medicine.created_date),
		'dist_id':str(medicine.dist_id),
		'medicine_name':str(medicine.medicine_name),
		'medicine_description':str(medicine.medicine_description),
		'medicine_contents':str(medicine.medicine_contents),
		'medicine_benifits':str(medicine.medicine_benifits),
		'medicine_alternatives':str(medicine.medicine_alternatives),
		'medicine_quantity':str(medicine.medicine_quantity),
		'medicine_measuringunit':str(medicine.medicine_measuringunit),
		'medicine_1stripequals':str(medicine.medicine_1stripequals),
		'medicine_costprice':str(medicine.medicine_costprice),
		'medicine_sellprice':str(medicine.medicine_sellprice),
		'medicine_mrp':str(medicine.medicine_mrp),
		'medicine_fixedrate':str(medicine.medicine_fixedrate),
		'medicine_discount':str(medicine.medicine_discount),
		'medicine_gst':str(medicine.medicine_gst),
		'prescription_required':str(medicine.prescription_required),
		'low_stock':str(medicine.low_stock),
		'contains_expired_stock':str(medicine.contains_expired_stock)
	}
	images=[]
	for x in MedicineImageData.objects.filter(medicine_id=medicine_id):
		images.append(x.medicine_image.url)
	data.update({'medicine_images':images})
	return data

def sendOTP(mobile):
	param={
	  "sender": "SABTEC",
	  "route": "4",
	  "country": "91",
	  "unicode": "1",
	  "sms": [
	    {
	      "message": "Test Message",
	      "to": [
	        mobile
	      ]
	    }
	  ]
	}
	res = requests.post(url='https://api.msg91.com/api/v2/sendsms', json=param, headers={'authkey':'350062AY5G7sGp95fe2ea92P1', 'Content-Type':'application/json'})
	res = res.json()
	if res['type'] == 'success':
		return True
	else:
		return False

def get_transactions(trans_type, store_id):
	lt=[]
	if trans_type == 0:
		for x in CartData.objects.filter(store_id=store_id):
			dic={
				'date':x.cart_date,
				'transaction_id':x.cart_id,
				'customer_id':x.customer_id,
				'total_amount':x.total_amount,
				'total_tax':x.total_tax_amount,
				'total_discount':x.total_discount_amount,
				'total_amount_to_pay':x.total_amount_to_pay
			}
			lt.append(dic)
		return lt
	elif trans_type == 1:
		for x in BillData.objects.filter(store_id=store_id):
			dic={
				'date':x.bill_date,
				'transaction_id':x.bill_id,
				'customer_id':x.customer_id,
				'total_amount':x.total_amount,
				'total_tax':x.total_tax_amount,
				'total_discount':x.total_discount_amount,
				'total_amount_to_pay':x.total_amount_to_pay
			}
			lt.append(dic)
		return lt
	elif trans_type == 2:
		dic={
			'incomplete_transactions':get_transactions(0, store_id),
			'complete_transactions':get_transactions(1, store_id)
		}
		return dic