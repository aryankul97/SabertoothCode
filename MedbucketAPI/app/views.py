from django.views.decorators.csrf import *
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
import datetime
from django.http import HttpResponse
from app.myutil import *
from django.core import serializers
from django.conf import settings
import os
from app.pdfutil import *
from app.botoutil import *

s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)

#To check mobile number uniqueness
@api_view(['POST'])
@csrf_exempt
def check_mobile_uniqueness(request):
	try:
		data=request.data
		mobile=data['mobile']
		if UserData.objects.filter(user_mobile=mobile).exists():
			data={'unique':False,'msg':'Mobile Number Already Exists'}
			return success_response(data)
		else:
			data={'unique':True,'msg':'Mobile Number Does Not Exists'}
			return success_response(data)
	except:
		return get_internal_error()

#To check email uniqueness
@api_view(['POST'])
@csrf_exempt
def check_email_uniqueness(request):
	try:
		data=request.data
		email=data['email']
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			if UserData.objects.filter(user_email=email, user_id=user_id).exists():
				data={'unique':False,'unique_code':888,'msg':'Email already registered with this account'}
				return success_response(data)
			elif UserData.objects.filter(user_email=email).exists():
				data={'unique':False,'unique_code':999,'msg':'Email already registered with other account'}
				return success_response(data)
			else:
				data={'unique':True,'unique_code':1000,'msg':'Email Does Not Exists'}
				return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def save_unit(request):
#	try:
		data=request.data
		unit=data['unit']
		subunits=data['subunits']
		if UnitData.objects.filter(unit=unit).exists():
			data={'msg':'Unit Already Exists'}
			return failure_response(data)
		else:
			u="UNIT"
			x=1
			uid=u+str(x)
			while UnitData.objects.filter(unit_id=uid).exists():
				x=x+1
				uid=u+str(x)
			UnitData(unit_id=uid, unit=unit).save()
			for sb in subunits:
				s="SUBUNIT"
				x=1
				sid=s+str(x)
				while SubunitData.objects.filter(subunit_id=sid).exists():
					x=x+1
					sid=s+str(x)
				SubunitData(subunit_id=sid, subunit_for=uid, subunit=sb).save()
			data={'msg':'Unit Created Successfully'}
			return success_response(data)
#	except:
#		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def list_unit(request):
	try:
		units=[]
		for unit in UnitData.objects.all():
			subunits=[]
			dic={'unit_id':unit.unit_id, 'unit':unit.unit}
			for sb in SubunitData.objects.filter(subunit_for=unit.unit_id):
				dic2={'subunit_id':sb.subunit_id, 'subunit':sb.subunit}
				subunits.append(dic2)
			dic.update({'subunits':subunits})
			units.append(dic)
		return success_response(units)
	except:
		return get_internal_error()

#To login user and generate auth token
@api_view(['POST'])
@csrf_exempt
def login_user(request):
	try:
		data=request.data
		mobile=data['mobile']
		if UserData.objects.filter(user_mobile=mobile).exists():
			user=UserData.objects.filter(user_mobile=mobile)[0]
			store=StoreData.objects.filter(user_id=user.user_id)[0]
			data={'user_type':0, 'user_authorization_token':get_userid_Authorization(user.user_id), 'store_id':str(store.store_id), 'user_data':get_user_data(user.user_id), 'msg':'User Logged In Successfully'}
			return success_response(data)
		else:
			u="U00"
			x=1
			uid=u+str(x)
			while UserData.objects.filter(user_id=uid).exists():
				x=x+1
				if x >= 10:
					u="U0"
				if x >= 100:
					u="U"
				uid=u+str(x)
			x=int(x)
			s="S00"
			x=1
			sid=s+str(x)
			while StoreData.objects.filter(store_id=sid).exists():
				x=x+1
				if x >= 10:
					s="S0"
				if x >= 100:
					u="S"
				sid=s+str(x)
			x=int(x)
			UserData(user_id=uid, user_mobile=mobile).save()
			StoreData(user_id=uid, store_id=sid).save()
			user=UserData.objects.filter(user_mobile=mobile)[0]
			data={'user_type':1, 'user_authorization_token':get_userid_Authorization(user.user_id), 'store_id':sid, 'user_data':get_user_data(user.user_id), 'msg':'User Logged In Successfully'}
			return success_response(data)
	except:
		return get_internal_error()

#To save user details
@api_view(['POST'])
@csrf_exempt
def save_user_details(request):
	try:
		data=request.data
		name=data['name']
		email=data['email']
		mobile=data['mobile']
		update_date=str(datetime.datetime.today())
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			UserData.objects.filter(user_id=user_id).update(updated_record_date=update_date, user_name=name, user_email=email, user_mobile=mobile)
			data={'msg':'Changes Saved Successfully', 'user_data':get_user_data(user_id)}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get user details
@api_view(['GET'])
@csrf_exempt
def get_user_details(request):
	try:
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			data={'user_data':get_user_data(user_id)}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To create store and generate store id
@api_view(['POST'])
@csrf_exempt
def update_store(request):
	try:
		data=request.data
		store_id=data['store_id']
		store_name=data['store_name']
		store_email=data['store_email']
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			if StoreData.objects.filter(store_name=store_name, store_email=store_email).exists() or StoreData.objects.filter(store_email=store_email).exists():
				data={'msg':'Store Name or Email Already Exists!'}
				return failure_response(data)			
			else:	
				StoreData.objects.filter(store_id=store_id).update(store_email=store_email, store_name=store_name)
				data={'msg':'Store Updated!'}
				return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To update store details and bank details
@api_view(['POST'])
@csrf_exempt
def update_store_and_bank_details(request):
	try:
		data=request.data
		store_id=data['store_id']
		store_name=data['store_name']
		store_email=data['store_email']
		bank_details=data['bank_details']
		gst_tin=data['gst_tin']
		billing_address=data['billing_address']
		upi_id=data['upi_id']
		store_logo=data['store_logo']
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			for x in StoreData.objects.filter(store_email=store_email):
				if not x.store_id == store_id:
					data={'msg':'Store Email Already Exists.'}
					return failure_response(data)
			for x in StoreData.objects.filter(store_name=store_name):
				if not x.store_id == store_id:
					data={'msg':'Store Name Already Exists.'}
					return failure_response(data)			
			StoreData.objects.filter(store_id=store_id).update(
				store_email=store_email,
				store_name=store_name,
				store_address=billing_address,
				store_gsttin=gst_tin,
				store_bank=bank_details,
				store_upiid=upi_id
			)
			StoreLogoData.objects.filter(store_id=store_id).delete()
			StoreLogoData(
				store_id=store_id,
				store_logo=store_logo
			).save()
			data={'msg':'Store details and bank details updated success_response.'}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get store details and bank details
@api_view(['POST'])
@csrf_exempt
def get_store_profile(request):
	try:
		data=request.data
		store_id=data['store_id']
		Authorization=request.META.get('HTTP_TOKEN')
		user_id=get_user_id_from_Authorization(Authorization)
		if check_Authorization(Authorization):
			store = StoreData.objects.filter(store_id=store_id)[0]
			store_logo = ''
			try:
				store_logo = StoreLogoData.objects.filter(store_id=store_id)[0].store_logo.url
			except IndexError:
				store_logo = 'N/A'
			data={
				'store_id':str(store.store_id),
				'store_name':str(store.store_name),
				'store_email':str(store.store_email),
				'bank_details':str(store.store_bank),
				'gst_tin':str(store.store_gsttin),
				'billing_address':str(store.store_address),
				'upi_id':str(store.store_upiid),
				'store_logo':str(store_logo)
			}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To save store payment and other details
@api_view(['POST'])
@csrf_exempt
def save_store_payment_and_business_details(request):
	try:
		data=request.data
		store_id=data['store_id']
		bank_account=data['bank_account']
		upi_id=data['upi_id']
		gst_tin=data['gst_tin']
		store_address=data['store_address']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			StoreData.objects.filter(store_id=store_id,user_id=get_user_id_from_Authorization(Authorization)).update(

				store_bank=bank_account,
				store_gsttin=gst_tin,
				store_address=store_address,
				store_upiid=upi_id
				)
			data={'msg':'Store Details Saved!','store_id':store_id}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get medicine info from master db
@api_view(['POST'])
@csrf_exempt
def get_medicine_basic_info_from_master(request):
	try:
		data=request.data
		medicine_name=data['medicine_name']
		medicine_name=medicine_name.upper()
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if MedicineMasterData.objects.filter(medicine_master_name=medicine_name).exists():
				medicine=MedicineMasterData.objects.filter(medicine_master_name=medicine_name)[0]
				data={
					'found':True,
					'name':str(medicine.medicine_master_name),
					'description':str(medicine.medicine_master_description),
					'contents':str(medicine.medicine_master_contents),
					'benifits':str(medicine.medicine_master_benifits),
					'alternatives':str(medicine.medicine_master_alternatives)
					}
				return success_response(data)
			else:
				data={'found':False}
				return failure_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To add medicine to store
@api_view(['POST'])
@csrf_exempt
def add_medicine_basic_info(request):
	try:
		data=request.data
		store_id=data['store_id']
		name=data['name']
		description=data['description']
		contents=data['contents']
		benifits=data['benifits']
		alternatives=data['alternatives']
		image=data['image']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if MedicineData.objects.filter(medicine_name=name, store_id=store_id).exists():
				data={'msg':'Medicine Already Exists'}
				return failure_response(data)
			else:
				m="M000"
				x=1
				mid=m+str(x)
				while MedicineData.objects.filter(medicine_id=mid).exists():
					x=x+1
					if x>=10:
						m='M00'
					if x>=100:
						m='M0'
					if x>=1000:
						m='M'
					mid=m+str(x)
				x=int(x)
				MedicineData(
					medicine_id=mid,
					store_id=store_id,
					medicine_name=name,
					medicine_description=description,
					medicine_contents=contents,
					medicine_benifits=benifits,
					medicine_alternatives=alternatives
				).save()
				MedicineImageData(
					medicine_id=mid,
					medicine_image=image
				).save()
				if not MedicineMasterData.objects.filter(medicine_master_name=name).exists():
					ms="MS000"
					x=1
					msid=ms+str(x)
					while MedicineMasterData.objects.filter(medicine_master_id=msid).exists():
						x=x+1
						if x>=10:
							ms="MS00"
						if x>=100:
							ms="MS0"
						if x>=1000:
							ms="MS"
						msid=ms+str(x)
					x=int(x)
					MedicineMasterData(
						medicine_master_id=mid,
						medicine_master_name=name.upper(),
						medicine_master_description=description,
						medicine_master_contents=contents,
						medicine_master_benifits=benifits,
						medicine_master_alternatives=alternatives
					).save()
				data={'store_id':store_id, 'msg':'Medicine Added!','medicine_id':mid}
				return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To add medicine stocks
@api_view(['POST'])
@csrf_exempt
def add_medicine_batch(request):
	try:
		if request.method=='POST':
			data=request.data
			medicine_id=data['medicine_id']
			quantity=data['quantity']
			expiry_date=data['expiry_date']
			batch_number=data['batch_number']
			Authorization=request.META.get('HTTP_TOKEN')
			if check_Authorization(Authorization):
				if not MedicineData.objects.filter(medicine_id=medicine_id).exists():
					data={'msg':'Incorrect Medicine ID'}
					return failure_response(data)
				elif MedicineBatchData.objects.filter(batch_number=batch_number).exists():
					data={'msg':'Batch Number Already Exists'}
					return failure_response(data)
				else:
					m="BAT000"
					x=1
					mid=m+str(x)
					while MedicineBatchData.objects.filter(batch_id=mid).exists():
						x=x+1
						if x>=10:
							m='BAT00'
						if x>=100:
							m='BAT0'
						if x>=1000:
							m='BAT'
						mid=m+str(x)
					x=int(x)
					MedicineBatchData(
						batch_id=mid,
						medicine_id=medicine_id,
						batch_number=batch_number,
						quantity=quantity,
						expiry_date=expiry_date
					).save()
					data={'msg':'Medicine Batch Added', 'batch_list':get_batch_data(medicine_id)}
					return success_response(data)
			else:
				return get_auth_token_error()
		else:
			return get_internal_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def get_medicine_batch(request):
	try:
		if request.method=='POST':
			data=request.data
			medicine_id=data['medicine_id']
			Authorization=request.META.get('HTTP_TOKEN')
			if check_Authorization(Authorization):
				if not MedicineData.objects.filter(medicine_id=medicine_id).exists():
					data={'msg':'Incorrect Medicine ID'}
					return failure_response(data)
				else:
					data={'batch_list':get_batch_data(medicine_id)}
					return success_response(data)
			else:
				return get_auth_token_error()
		else:
			return get_internal_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def delete_medicine_batch(request):
	try:
		if request.method=='POST':
			data=request.data
			batch_id=data['batch_id']
			Authorization=request.META.get('HTTP_TOKEN')
			if check_Authorization(Authorization):
				if MedicineBatchData.objects.filter(batch_id=batch_id).exists():
					MedicineBatchData.objects.filter(batch_id=batch_id).update(status='0')
					data={'msg':'Batch Deleted Successfully'}
					return success_response(data)
				else:
					data={'msg':'Incorrect Batch ID'}
					return failure_response(data)
			else:
				return get_auth_token_error()
		else:
			return get_internal_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def update_medicine_batch(request):
	try:
		if request.method=='POST':
			data=request.data
			batch_id=data['batch_id']
			quantity=data['quantity']
			expiry_date=data['expiry_date']
			batch_number=data['batch_number']
			Authorization=request.META.get('HTTP_TOKEN')
			if check_Authorization(Authorization):
				if MedicineBatchData.objects.filter(batch_id=batch_id).exists():
					MedicineBatchData.objects.filter(batch_id=batch_id).update(
						batch_number=batch_number,
						quantity=quantity,
						expiry_date=expiry_date
					)
					data={'msg':'Batch Updated Successfully'}
					return success_response(data)
				else:
					data={'msg':'Incorrect Batch ID'}
					return failure_response(data)
			else:
				return get_auth_token_error()
		else:
			return get_internal_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def add_medicine_stocks(request):
	try:
		data=request.data
		medicine_id=data['medicine_id']
		unit=data['unit']
		onestripequals=data['one_stripe_equals']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			MedicineData.objects.filter(medicine_id=medicine_id).update(
				medicine_quantity=get_total_medicine_quatity(medicine_id),
				medicine_measuringunit=unit,
				medicine_1stripequals=onestripequals
				)
			data={'msg':'Medicine Stock Added!','medicine_id':medicine_id}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To add medicine price
@api_view(['POST'])
@csrf_exempt
def add_medicine_price(request):
	try:
		data=request.data
		medicine_id=data['medicine_id']
		costprice=data['cost_price']
		sellprice=data['sell_price']
		mrp=data['mrp']
		fixedrate=data['fixed_rate']
		discount=data['discount']
		gst=data['gst']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			MedicineData.objects.filter(medicine_id=medicine_id).update(
				medicine_costprice=costprice,
				medicine_sellprice=sellprice,
				medicine_mrp=mrp,
				medicine_fixedrate=fixedrate,
				medicine_discount=discount,
				medicine_gst=gst
				)
			data={'msg':'Medicine Price Updated!','medicine_id':medicine_id}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To add medicine distributer
@api_view(['POST'])
@csrf_exempt
def add_medicine_distributer(request):
	try:
		data=request.data
		store_id=data['store_id']
		medicine_id=data['medicine_id']
		name=data['name']
		mobile=data['mobile']
		email=data['email']
		address=data['address']
		balance=data['balance']
		gst=data['gst']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if DistributerData.objects.filter(dist_name=name.upper()).exists():
				MedicineData.objects.filter(medicine_id=medicine_id).update(
					dist_id=DistributerData.objects.filter(dist_name=name.upper())[0].dist_id,
					status='1'
				)
				data={'msg':'Medicine Activated Successfully!','medicine_id':medicine_id}
				return success_response(data)
			else:
				d="D00"
				x=1
				did=d+str(x)
				while DistributerData.objects.filter(dist_id=did).exists():
					x=x+1
					did=d+str(x)
				x=int(x)
				DistributerData(
					dist_id=did,
					store_id=store_id,
					dist_name=name.upper(),
					dist_email=email,
					dist_mobile=mobile,
					dist_address=address,
					dist_gstin=gst,
					dist_balance=balance,
					).save()
				MedicineData.objects.filter(medicine_id=medicine_id).update(
					dist_id=did,
					status='1'
				)
				data={'msg':'Medicine Activated Successfully!','medicine_id':medicine_id}
				return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get medicine data
@api_view(['POST'])
@csrf_exempt
def get_medicine_data(request):
	try:
		data=request.data
		medicine_id=data['medicine_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if MedicineData.objects.filter(medicine_id=medicine_id, status='1').exists():
				medicine=MedicineData.objects.filter(medicine_id=medicine_id, status='1')[0]
				dic=get_medicine_info(medicine_id)
				data={
					'medicine_data':get_medicine_info(medicine_id),
					'stock':{'quantity':dic['medicine_quantity'], 'measuring_unit':dic['medicine_measuringunit'], '1stripequals':dic['medicine_1stripequals']},
					'price':{'cost_price':dic['medicine_costprice'], 'sell_price':dic['medicine_sellprice'], 'mrp':dic['medicine_mrp'], 'fixed_rate':dic['medicine_fixedrate']},
					'distributer_data':get_distributer_data(medicine.dist_id)
					}
				return success_response(data)
			else:
				data={'msg':'Incorrect Medicine ID / Medicine Not Found'}
				return failure_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get medicine suggestions
@api_view(['POST'])
@csrf_exempt
def get_medicine_suggestions(request):
#	try:
		data=request.data
		store_id=data['store_id']
		keyword=str(data['keyword'])
		Authorization=request.META.get('HTTP_TOKEN')
		MedicineData.objects.all().update(status='1')
		if check_Authorization(Authorization):
			suggestions=get_suggestions_id(store_id, keyword)
			data={'suggestions':suggestions}
			return success_response(data)
		else:
			return get_auth_token_error()
#	except:
#		return get_internal_error()

#To get medicine details
@api_view(['POST'])
@csrf_exempt
def get_medicines_details(request):
	try:
		data=request.data
		medicine_id=data['medicines_ids']
		store_id=data['store_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			medicines=[]
			for elt in medicine_id:
				medicines.append(get_medicine_info(elt))
			data={'medicines_details':medicines}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To save purchase details
@api_view(['POST'])
#@parser_classes([JSONParser])
@csrf_exempt
def save_purchse_review_details(request):
	try:
		data=request.data
		store_id=data['store_id']
		medicines_data=data['medicines_data']
		cart_id=create_cart_id(store_id)
		Authorization=request.META.get('HTTP_TOKEN')
		total_amount=0.0
		total_tax_amount=0.0
		total_discount_amount=0.0
		total_amount_to_pay=0.0
		if check_Authorization(Authorization):
			for elt in medicines_data:
				CartItemData(
					cart_id=cart_id,
					medicine_id=elt['medicine_id'],
					store_id=store_id,
					quantity=elt['quantity'],
					amount=elt['amount'],
					tax_amount=elt['tax_amount'],
					discount_amount=elt['discount_amount'],
					amount_to_pay=float(elt['amount'])+float(elt['tax_amount'])-float(elt['discount_amount'])
					).save()
				total_amount_to_pay=total_amount_to_pay+float(elt['amount'])+float(elt['tax_amount'])-float(elt['discount_amount'])
				total_tax_amount=total_tax_amount+float(elt['tax_amount'])
				total_discount_amount=total_discount_amount+float(elt['discount_amount'])
				total_amount=total_amount+float(elt['amount'])
			CartData.objects.filter(cart_id=cart_id).update(
				total_amount=str(total_amount),
				total_tax_amount=str(total_tax_amount),
				total_discount_amount=str(total_discount_amount),
				total_amount_to_pay=str(total_amount_to_pay)
				)
			data={'msg':'Items Successfully Added To Cart','cart_id':cart_id}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get customer details
@api_view(['POST'])
@csrf_exempt
def get_customer_details(request):
	try:
		data=request.data
		customer_name=data['customer_name']
		store_id=data['store_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			return success_response(get_customer_suggestions_id(store_id, customer_name))
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To save customer details and get total amount
@api_view(['POST'])
@csrf_exempt
def save_customer_details_and_get_total_amount(request):
	try:
		data=request.data
		customer_name=data['customer_name']
		customer_mobile=data['customer_mobile']
		customer_address=data['customer_address']
		customer_doctor=data['customer_doctor']
		store_id=data['store_id']
		cart_id=data['cart_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if StoreCustomerData.objects.filter(customer_name=customer_name).exists():
				customer=StoreCustomerData.objects.filter(customer_name=customer_name)[0]
				CartData.objects.filter(cart_id=cart_id).update(
					customer_id=customer.customer_id
				)
				cart=CartData.objects.filter(cart_id=cart_id)[0]
				data={'total_amount':str(cart.total_amount), 'total_tax_amount':str(cart.total_tax_amount), 'total_discount_amount':str(cart.total_discount_amount), 'total_amount_to_pay':str(cart.total_amount_to_pay)}
				return success_response(data)
			else:
				c="CUS00"
				x=1
				cic=c+str(x)
				while StoreCustomerData.objects.filter(customer_id=cic).exists():
					x=x+1
					cic=c+str(x)
				x=int(x)
				StoreCustomerData(
					customer_id=cic,
					store_id=store_id,
					customer_name=customer_name,
					customer_mobile=customer_mobile,
					customer_address=customer_address,
					customer_doctor=customer_doctor,
				).save()
				CartData.objects.filter(cart_id=cart_id).update(
					customer_id=cic
				)
				cart=CartData.objects.filter(cart_id=cart_id)[0]
				{'total_amount':str(cart.total_amount), 'total_tax_amount':str(cart.total_tax_amount), 'total_discount_amount':str(cart.total_discount_amount), 'total_amount_to_pay':str(cart.total_amount_to_pay)}
				return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To record payment info
@api_view(['POST'])
@csrf_exempt
def record_payment_info(request):
#	try:
		data=request.data
		store_id=data['store_id']
		cart_id=data['cart_id']
		pay_mode=data['pay_mode']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if pay_mode=='Online':
				transaction_id=data['transaction_id']
				cart=CartData.objects.filter(cart_id=cart_id)[0]
				items=CartItemData.objects.filter(cart_id=cart_id)
				bill_id=create_bill_id(store_id)
				BillData(
					bill_id=bill_id,
					customer_id=cart.customer_id,
					store_id=cart.store_id,
					total_amount=cart.total_amount,
					total_tax_amount=cart.total_tax_amount,
					total_discount_amount=cart.total_discount_amount,
					total_amount_to_pay=cart.total_amount_to_pay,
					pay_mode='1',
					transaction_id=transaction_id,
				).save()
				for x in items:
					BillItemData(
						bill_id=bill_id,
						medicine_id=x.medicine_id,
						store_id=x.tax_amount,
						quantity=x.quantity,
						amount=x.amount,
						tax_amount=x.tax_amount,
						discount_amount=x.discount_amount,
						amount_to_pay=x.amount_to_pay
					).save()
					med=MedicineData.objects.filter(medicine_id=x.medicine_id)[0]
					if med.medicine_quantity == 'Not Availi' or '':
						new_quantity=0.0-float(x.quantity)
					else:
						new_quantity=float(med.medicine_quantity)-float(x.quantity)
						
					if new_quantity < 50.0:
						MedicineData.objects.filter(medicine_id=x.medicine_id).update(medicine_quantity=str(new_quantity), low_stock='1')
					else:
						MedicineData.objects.filter(medicine_id=x.medicine_id).update(medicine_quantity=str(new_quantity))
				get_bill_pdf(BillData.objects.filter(bill_id=bill_id)[0], BillItemData.objects.filter(bill_id=bill_id), StoreCustomerData.objects.filter(customer_id=cart.customer_id)[0])
				pdf_name=bill_id+'.pdf'
				with open(pdf_name, "rb") as f:
					s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, Key=f.name)	
					pdf_url='https://%s/%s' % (settings.AWS_S3_CUSTOM_DOMAIN, f.name)
				os.remove(pdf_name)
				BillData.objects.filter(bill_id=bill_id).update(bill_pdf_url=pdf_url)
				data={'bill_data':serializers.serialize('json', BillData.objects.filter(bill_id=bill_id)),'bill_items_data':serializers.serialize('json', BillItemData.objects.filter(bill_id=bill_id))}
				return success_response(data)
			else:
				cart=CartData.objects.filter(cart_id=cart_id)[0]
				items=CartItemData.objects.filter(cart_id=cart_id)
				bill_id=create_bill_id(store_id)
				BillData(
					bill_id=bill_id,
					customer_id=cart.customer_id,
					store_id=cart.store_id,
					total_amount=cart.total_amount,
					total_tax_amount=cart.total_tax_amount,
					total_discount_amount=cart.total_discount_amount,
					total_amount_to_pay=cart.total_amount_to_pay,
					pay_mode='2'
				).save()
				for x in items:
					BillItemData(
						bill_id=bill_id,
						medicine_id=x.medicine_id,
						store_id=store_id,
						quantity=x.quantity,
						amount=x.amount,
						tax_amount=x.tax_amount,
						discount_amount=x.discount_amount,
						amount_to_pay=x.amount_to_pay
					).save()
					med=MedicineData.objects.filter(medicine_id=x.medicine_id)[0]
					if med.medicine_quantity == 'Not Availi' or '':
						new_quantity=0.0-float(x.quantity)
					else:
						new_quantity=float(med.medicine_quantity)-float(x.quantity)
					if new_quantity < 50.0:
						MedicineData.objects.filter(medicine_id=x.medicine_id).update(medicine_quantity=str(new_quantity), low_stock='1')
					else:
						MedicineData.objects.filter(medicine_id=x.medicine_id).update(medicine_quantity=str(new_quantity))
				get_bill_pdf(BillData.objects.filter(bill_id=bill_id)[0], BillItemData.objects.filter(bill_id=bill_id), StoreCustomerData.objects.filter(customer_id=cart.customer_id)[0])
				pdf_name=bill_id+'.pdf'
				with open(pdf_name, "rb") as f:
					s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, Key=f.name)	
					pdf_url='https://%s/%s' % (settings.AWS_S3_CUSTOM_DOMAIN, f.name)
				os.remove(pdf_name)
				BillData.objects.filter(bill_id=bill_id).update(bill_pdf_url=pdf_url)
				data={'bill_data':serializers.serialize('json', BillData.objects.filter(bill_id=bill_id)),'bill_items_data':serializers.serialize('json', BillItemData.objects.filter(bill_id=bill_id))}
				return success_response(data)
		else:
			return get_auth_token_error()
#	except:
#		return get_internal_error()

#To get inventory listing
@api_view(['POST'])
@csrf_exempt
def get_inventory_listing(request):
	try:
		data=request.data
		store_id=data['store_id']
		Authorization=request.META.get('HTTP_TOKEN')
		lt=[]
		if check_Authorization(Authorization):
			inventory_data=MedicineData.objects.filter(store_id=store_id, status='1')
			for x in inventory_data:
				med=MedicineData.objects.filter(medicine_id=x.medicine_id, status='1')[0]
				tablet_quantity = 0
				if med.medicine_measuringunit == 'Strip':
					tablet_quantity = float(med.medicine_quantity) * float(med.x.medicine_1stripequals)
				elif med.medicine_measuringunit == 'Tablet':
					tablet_quantity = str(med.medicine_quantity)
				else:
					tablet_quantity = 0
				dic={
					'medicine_id':x.medicine_id,
					'distributer_id':x.dist_id,
					'medicine_name':x.medicine_name,
					'description':x.medicine_description,
					'contents':x.medicine_contents,
					'benefits':x.medicine_benifits,
					'alternatives':x.medicine_alternatives,
					'quantity':x.medicine_quantity,
					'tablet_quantity':tablet_quantity,
					'measuring_unit':x.medicine_measuringunit,
					'1_strip_equals':x.medicine_1stripequals,
					'cost_price':x.medicine_costprice,
					'sell_price':x.medicine_sellprice,
					'mrp':x.medicine_mrp,
					'fixedrate':x.medicine_fixedrate,
					'discount':x.medicine_discount,
					'gst':x.medicine_gst
				}
				lt.append(dic)
			data={'inventory_data':lt}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def update_stock(request):
	try:
		data=request.data
		store_id=data['store_id']
		medicine_id=data['medicine_id']
		updated_quantity=data['updated_quantity']
		quantity_type=data['quantity_type']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			if MedicineData.objects.filter(medicine_id=medicine_id, status='1').exists():
				med=MedicineData.objects.filter(medicine_id=medicine_id, status='1')[0]
				if quantity_type == med.medicine_measuringunit:
					MedicineData.objects.filter(medicine_id=medicine_id, status='1').update(
						quantity=updated_quantity
					)
				elif quantity_type == 'Tablet' and med.medicine_measuringunit == 'Strip':
					stripequals=float(med.medicine_1stripequals)
					updated_quantity=float(updated_quantity)/stripequals
					MedicineData.objects.filter(medicine_id=medicine_id, status='1').update(
						quantity=str(updated_quantity)
					)
				else:
					data={'msg':'ERROR : Incorrect Measurning Unit. Medicine Measurning Unit is '+str(med.medicine_measuringunit)+' but you have sent '+quantity_type+' measurning unit.'}
					return failure_response(data)
				data={'msg':'Medicine Stock Updated!'}
				return success_response(data)
			else:
				data={'msg':'Incorrect Medicine ID'}
				return failure_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To get medicine stock data
@api_view(['POST'])
@csrf_exempt
def get_selected_medicine_stock_data(request):
	try:
		data=request.data
		store_id=data['store_id']
		medicine_id=data['medicine_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			medicine=MedicineData.objects.filter(medicine_id=medicine_id)[0]
			data={'medicine_name':str(medicine.medicine_name),'quantity':str(medicine.medicine_quantity),'medicine_measuringunit':str(medicine.medicine_measuringunit),'medicine_1stripequals':str(medicine.medicine_1stripequals)}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

#To update medicine stock data
@api_view(['POST'])
@csrf_exempt
def update_medicine_stock_data(request):
	try:
		data=request.data
		store_id=data['store_id']
		medicine_id=data['medicine_id']
		update_quantity=data['update_quantity']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			medicine=MedicineData.objects.filter(medicine_id=medicine_id)
			medicine.update(medicine_quantity=update_quantity)
			medicine=MedicineData.objects.filter(medicine_id=medicine_id)[0]
			data={'msg':'Stock Updated!','medicine_name':str(medicine.medicine_name),'quantity':str(medicine.medicine_quantity),'medicine_measuringunit':str(medicine.medicine_measuringunit),'medicine_1stripequals':str(medicine.medicine_1stripequals)}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def get_dashboard_data(request):
	try:
		data=request.data
		store_id=data['store_id']
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			data={
				'low_stocks':get_number_of_low_stocks(store_id),
				'expired_stocks':get_number_of_expired_stocks(store_id),
				'today_revenue':get_today_revenue(store_id),
				'total_stocks_value':get_total_stocks_value(store_id),
				'total_revenue':get_total_revenue(store_id),
				'complete_transactions':get_complete_transaction_data(store_id),
				'drafted_transactions':get_incomplete_transaction_data(store_id),
			}
			return success_response(data)
		else:
			return get_auth_token_error()
	except:
		return get_internal_error()

@api_view(['POST'])
@csrf_exempt
def get_transactions_data(request):
#	try:
		data=request.data
		store_id=data['store_id']
		trans_type=int(data['trans_type'])
		Authorization=request.META.get('HTTP_TOKEN')
		if check_Authorization(Authorization):
			return success_response(get_transactions(trans_type, store_id))
		else:
			return get_auth_token_error()
#	except:
#		return get_internal_error()

@csrf_exempt
def trial(request):
	MedicineData.objects.all().update(status='1')
	return HttpResponse('Done')