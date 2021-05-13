from django.contrib.auth.models import User
from app.myutil import *
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from app.models import *
from django.core import serializers
import csv
import pandas as pd
from wsgiref.util import FileWrapper
import mimetypes
import os

@csrf_exempt
@api_view(["POST"])
def login(request):
	if request.method=='POST':
		data=request.data
		username = data["username"]
		password = data["password"]
		if username is None or password is None:
			data={'msg':'Please provide both username and password'}
			return get_failure_response(data)
		if AdminData.objects.filter(username=username, password=password).exists():
			admin=AdminData.objects.filter(username=username)[0]
			data={'user_authorization_token':get_admin_authorization(admin.admin_id), 'role_id':'100', 'admin':True, 'staff':False, 'msg':'Admin Logged In Successfully'}
			return get_success_response(data)
		elif StaffData.objects.filter(username=username,password=password,status='1').exists():
			staff=StaffData.objects.filter(username=username)[0]
			data={'user_authorization_token':get_staff_authorization(staff.staff_id),'staff_type_id':str(staff.staff_type_id), 'role_id':str(StaffTypeData.objects.filter(staff_type_id=staff.staff_type_id)[0].role_id), 'admin':False, 'staff':True, 'msg':'Staff Logged In Successfully'}
			return get_success_response(data)
		else:
			data={'msg':'Invalid Credentials'}
			return get_failure_response(data)
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def forgot_password(request):
	if request.method=='POST':
		data=request.data
		username=data['username']
		if StaffData.objects.filter(username=username).exists():
			staff=StaffData.objects.filter(username=username)[0]
			otp=str(uuid.uuid5(uuid.NAMESPACE_DNS, str(staff.staff_id)+str(datetime.datetime.today())).int)
			otp=otp[:6]
			if sendOTP(str(staff.mobile), otp):
				data={'generated_otp':otp, 'staff_id':str(staff.staff_id), 'staff_account':True, 'admin_account':False}
				return get_success_response(data)
			else:
				data={'msg':'Unable to send OTP'}
				return get_failure_response(data)
		elif AdminData.objects.filter(username=username).exists():
			admin=AdminData.objects.filter(username=username)[0]
			otp=str(uuid.uuid5(uuid.NAMESPACE_DNS, str(admin.admin_id)+str(datetime.datetime.today())).int)
			otp=otp[:6]
			if sendOTP(str(admin.mobile), otp):
				data={'generated_otp':otp, 'admin_id':str(admin.admin_id), 'staff_account':False, 'admin_account':True}
				return get_success_response(data)
			else:
				data={'msg':'Unable to send OTP'}
				return get_failure_response(data)
		else:
			data={'msg':'Incorrect Username'}
			return get_failure_response(data)
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def change_password(request):
	if request.method=='POST':
		data=request.data
		staff_id=data['staff_id']
		password=data['password']
		if StaffData.objects.filter(staff_id=staff_id).exists():
			StaffData.objects.filter(staff_id=staff_id).update(password=password)
			data={'msg':'Password Updated Successfully'}
			return get_success_response(data)
		elif AdminData.objects.filter(admin_id=staff_id).exists():
			AdminData.objects.filter(admin_id=staff_id).update(password=password)
			data={'msg':'Password Updated Successfully'}
			return get_success_response(data)
		else:
			data={'msg':'Incorrect Staff ID'}
			return get_failure_response(data)
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def administrator(request):
	if request.method=='POST':
		data=request.data
		username=data['username']
		password=data['password']
		mobile=data['mobile']
		if AdminData.objects.filter(username=username).exists():
			data={'msg':'Admin Already Exists'}
			return get_failure_response(data)
		else:
			s="AD00"
			x=1
			sid=s+str(x)
			while AdminData.objects.filter(admin_id=sid).exists():
				x=x+1
				if x>=10:
					s='AD0'
				sid=s+str(x)
			x=int(x)
			AdminData(admin_id=sid, username=username, password=password, mobile=mobile).save()
			data={'msg':'Admin Created Successfully'}
			return get_success_response(data)
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def administrator_list(request):
	if request.method=='POST':
		dic={}
		lt=[]
		for x in AdminData.objects.all():
			dic={'admin_id':x.admin_id,'username':x.username, 'password':x.password}
			lt.append(dic)
		data={'admins':lt}
		return get_success_response(data)
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff_type(request):
	if request.method=='POST':
		data=request.data
		stafftype=str(data['stafftype']).upper()
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization):
			if StaffTypeData.objects.filter(staff_type_name=stafftype).exists():
				data={'msg':'Staff Type Already Exists'}
				return get_failure_response(data)
			else:
				s="ST00"
				x=1
				sid=s+str(x)
				while StaffTypeData.objects.filter(staff_type_id=sid).exists():
					x=x+1
					if x>=10:
						s='ST0'
					sid=s+str(x)
				x=int(x)
				role_id=get_role_id()
				StaffTypeData(staff_type_id=sid, staff_type_name=stafftype, role_id=role_id).save()
				data={'staff_type_id':sid, 'staff_type':stafftype, 'role_id':role_id, 'msg':'Staff Type Added Successfully'}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff_type_list(request):
	if request.method=='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization):
			dic={}
			lt=[]
			for x in StaffTypeData.objects.all():
				dic={'staff_type_id':x.staff_type_id, 'role_id':x.role_id, 'staff_type_name':x.staff_type_name}
				lt.append(dic)
			data={'staff_type':lt}
			return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#To login user and generate auth token
@api_view(['POST'])
@csrf_exempt
def vehicles(request):
	if request.method=='POST':
		data=request.data
		business_id = data['business_id']
		number_plate = data['number_plate']
		vehicle_name = data['vehicle_name']
		manufacturer = data['manufacturer']
		hazardous_license_expiry_date = change_dateformat(data['hazardous_license_expiry_date'])
		insurence_expiry_date = change_dateformat(data['insurence_expiry_date'])
		vehicle_photo = data['vehicle_photo']
		rc_number = data['rc_number']
		insurence_number = data['vehicle_insurance']
		puc=data['puc']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if VehiclesData.objects.filter(rc_number=rc_number).exists():
				data={'msg':'Vehicle Already Exists with Same RC Number'}
				return get_failure_response(data)
			else:
				v="V00"
				x=1
				vid=v+str(x)
				while VehiclesData.objects.filter(vehicle_id=vid).exists():
					x=x+1
					vid=v+str(x)
				x=int(x)
				VehiclesData(
					vehicle_id=vid,
					business_id=business_id,
					number_plate=number_plate,
					vehicle_name=vehicle_name,
					manufacturer=manufacturer,
					vehicle_photo=vehicle_photo,
					hazardous_license_expiry_date=hazardous_license_expiry_date,
					insurence_expiry_date=insurence_expiry_date,
					rc_number=rc_number,
					insurence_number=insurence_number,
					puc=puc
				).save()
				data={'msg':'Vehicle Added Successfully'}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	elif request.method=='GET':
		data = request.data
		business = data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if BusinessData.objects.filter(business_id=business).exists():
				data={'vehicles':get_vehicles_list(business)}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def vehicles_list(request):
	if request.method=='POST':
		data = request.data
		business = data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if BusinessData.objects.filter(business_id=business).exists():
				data={'vehicles':get_vehicles_list(business)}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def vehicle_delete(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data = request.data
			vehicle_id = data['vehicle_id']
			if VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').exists():
				VehiclesData.objects.filter(vehicle_id=vehicle_id).update(status='0')
				data={'msg':'Vehicle Deleted Successfully'}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def vehicle_update(request):
	if request.method =='POST':
		data=request.data
		vehicle_id = data['vehicle_id']
		number_plate = data['number_plate']
		vehicle_name = data['vehicle_name']
		manufacturer = data['manufacturer']
		hazardous_license_expiry_date = change_dateformat(data['hazardous_license_expiry_date'])
		insurence_expiry_date = change_dateformat(data['insurence_expiry_date'])
		rc_number = data['rc_number']
		insurence_number = data['vehicle_insurance']
		puc=data['puc']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').exists():
				VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').update(
					vehicle_id=vehicle_id,
					number_plate=number_plate,
					vehicle_name=vehicle_name,
					manufacturer=manufacturer,
					hazardous_license_expiry_date=hazardous_license_expiry_date,
					insurence_expiry_date=insurence_expiry_date,
					rc_number=rc_number,
					insurence_number=insurence_number,
					puc=puc
				)
				data={'msg':'Vehicle Updated Successfully'}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def vehicle_show(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data = request.data
			vehicle_id = data['vehicle_id']
			if VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').exists():
				vehicle=VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1')[0]
				data={
					'vehicle_id':str(vehicle.vehicle_id),
					'business_id':str(vehicle.business_id),
					'staff_id':str(vehicle.staff_id),
					'number_plate':str(vehicle.number_plate),
					'vehicle_name':str(vehicle.vehicle_name),
					'driver_assigned':str(vehicle.driver_assigned),
					'driver_name':str(vehicle.driver_name),
					'manufacturer':str(vehicle.manufacturer),
					'hazardous_license_expiry_date':str(vehicle.hazardous_license_expiry_date),
					'insurence_expiry_date':str(vehicle.insurence_expiry_date),
					'vehicle_photo':str(vehicle.vehicle_photo.url),
					'rc_number':str(vehicle.rc_number.url),
					'insurence_number':str(vehicle.insurence_number.url),
					'puc':str(vehicle.puc.url)
				}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff(request):
	if request.method =='POST':
		data = request.data
		business = data['business_id']
		staff_type_id = data['staff_type_id']
		fullname = data['fullname']
		username = data['username']
		mobile = data['phone_number']
		alternate_mobile = data['alternate_number']
		dob = data['dob']
		aadhar = data['aadhar_number']
		profile = data['profile_picture']
		driving_license = data['driving_license']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if StaffData.objects.filter(username=username).exists() or AdminData.objects.filter(username=username).exists():
				data={'msg':'Staff Username Already Exists'}
				return get_failure_response(data)
			else:
				password=str(uuid.uuid5(uuid.NAMESPACE_DNS, username).int)
				password=password[:6]
				s="S00"
				x=1 
				sid=s+str(x)
				while StaffData.objects.filter(staff_id=sid).exists():
					x=x+1
					if x>=10:
						s='S0'
					if x>=100:
						s='S'
					sid=s+str(x)
				x=int(x)
				StaffData(
					staff_id = sid,
					business_id = business,
					staff_type_id = staff_type_id,
					fullname = fullname,
					username = username,
					password = password,
					mobile = mobile,
					alternate_mobile = alternate_mobile,
					dob = dob,
					aadhar = aadhar,
					profile_picture = profile,
					driving_license = driving_license

				).save()
				data={'msg':'Staff Member Added Successfully', 'staff_username':username,'staff_password':password}
				return get_success_response(data)
		else:
			return get_auth_token_error()

@api_view(['POST'])
@csrf_exempt
def staff_list(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data = request.data
			business = data['business_id']
			if BusinessData.objects.filter(business_id=business).exists():
				data={'staff':get_staff_data(business)}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff_delete(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data = request.data
			staff_id = data['staff_id']
			if StaffData.objects.filter(staff_id=staff_id, status='1').exists():
				StaffData.objects.filter(staff_id=staff_id).update(status='0')
				VehiclesData.objects.filter(staff_id=staff_id).update(staff_id='N/A', driver_assigned='0', driver_name='N/A')
				data={'msg':'Staff Deleted Successfully'}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Staff ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff_update(request):
	if request.method =='POST':
		data = request.data
		staff_id = data['staff_id']
		fullname = data['fullname']
		mobile = data['phone_number']
		alternate_mobile = data['alternate_number']
		dob = data['dob']
		aadhar = data['aadhar_number']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			staff_id = data['staff_id']
			if StaffData.objects.filter(staff_id=staff_id, status='1').exists():
				StaffData.objects.filter(staff_id=staff_id, status='1').update(
					fullname = fullname,
					mobile = mobile,
					alternate_mobile = alternate_mobile,
					dob = dob,
					aadhar = aadhar
				)
				data={'msg':'Staff Updated Successfully'}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Staff ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def staff_show(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data = request.data
			staff_id = data['staff_id']
			if StaffData.objects.filter(staff_id=staff_id, status='1').exists():
				staff=StaffData.objects.filter(staff_id=staff_id, status='1')[0]
				data={
					'staff_id':str(staff.staff_id),
					'business_id':str(staff.business_id),
					'staff_type_id':str(staff.staff_type_id),
					'fullname':str(staff.fullname),
					'username':str(staff.username),
					'password':str(staff.password),
					'mobile':str(staff.mobile),
					'alternate_mobile':str(staff.alternate_mobile),
					'dob':str(staff.dob),
					'aadhar':str(staff.aadhar),
					'profile_picture':str(staff.profile_picture.url),
					'driving_license':str(staff.driving_license.url)
				}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Staff ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def assign_driver_to_vehicle(request):
	if request.method =='POST':
		data = request.data
		staff_id = data['staff_id']
		vehicle_id = data['vehicle_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').exists():
				data={'msg':'Vehicle Does Not Exists'}
				return get_failure_response(data)
			else:
				if not StaffData.objects.filter(staff_id=staff_id, staff_type_id='ST001', status='1').exists():
					data={'msg':'Driver Does Not Exists'}
					return get_failure_response(data)
				else:
					driver=StaffData.objects.filter(staff_id=staff_id, status='1')[0]
					VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').update(staff_id=staff_id,driver_assigned='1',driver_name=driver.fullname)
					data={'msg':'Driver Assigned!'}
					return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#Purchase Cylinder Stocks
@api_view(['POST'])
@csrf_exempt
def cylinder_bills(request):
	if request.method=='POST':
		data = request.data
		business_id = data['business_id']
		filled_cylinder_quantity = int(data['filled_cylinder_quantity'])
		empty_cylinder_sent = int(data['empty_cylinder_returned'])
		price_per_cylinder = float(data['price_per_cylinder'])
		paymode = data['paymode']
		total_price = float(data['total_price'])
		bill_date = data['date']
		bill = data['bill_pic']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				bid=generate_bill_id()
				if CylinderData.objects.filter(business_id=business_id).exists():
					cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
					if int(cylinder_data.total_empty_cylinder) < int(empty_cylinder_sent):
						data={'msg':"You don't have enough empty cylinders to purchase filled cylinders."}
						return get_failure_response(data)
				else:
					CylinderData(business_id=business_id).save()
					
				cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
					
				total_filled_cylinder=int(cylinder_data.total_filled_cylinder)+int(filled_cylinder_quantity)
				total_empty_cylinder=int(cylinder_data.total_empty_cylinder)-int(empty_cylinder_sent)
				total_cylinder=total_filled_cylinder+total_empty_cylinder

				CylinderData.objects.filter(business_id=business_id).update(
					total_filled_cylinder=str(total_filled_cylinder),
					total_empty_cylinder=str(total_empty_cylinder),
					total_cylinder=str(total_cylinder)
				)
				CylinderPurchaseData(
					bill_id=bid,
					business_id=business_id,
					quantity=str(filled_cylinder_quantity),
					slot_quantity=str(filled_cylinder_quantity),
					empty_cylinder_sent=str(empty_cylinder_sent),
					paymode=paymode,
					total_price=str(total_price),
					per_cylinder_price=str(price_per_cylinder),
					bill_date=bill_date,
					bill=bill
				).save()
				
				data={'msg':'Purchase Bill Saved and Stock Updated Successfully!', 'bill_id':bid}
				return get_success_response(data)
		else:
			return get_auth_token_error()

@api_view(['POST'])
@csrf_exempt
def cylinder_bills_list(request):
	if request.method =='POST':
		data = request.data
		business_id = data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if BusinessData.objects.filter(business_id=business_id).exists():
				data={'bills':get_cylinder_bills(business_id)}
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_cylinder_sales(request):
	if request.method =='POST':
		data = request.data
		business_id = data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if BusinessData.objects.filter(business_id=business_id).exists():
				data=get_cylinder_sales_from_util(business_id)
				return get_success_response(data)
			else:
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def business(request):
	if request.method =='POST':
		data=request.data
		business_name=data['business_name']
		business_pic=data['business_pic']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			b="B00"
			x=1
			bid=b+str(x)
			while BusinessData.objects.filter(business_id=bid).exists():
				x=x+1
				bid=b+str(x)
			x=int(x)
			BusinessData(business_id=bid, business_name=business_name, business_picture=business_pic).save()
			data={'business_data':get_business_data()}
			return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def business_list(request):
	if request.method =='POST':
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			data={'business_data':get_business_data()}
			return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def assign_cylinder(request):
	if request.method=='POST':
		data = request.data
		business_id = data['business_id']
		filled_quantity =int(data['filled_quantity'])
		current_cylinder_cost = float(data['current_cylinder_cost'])
		assign_date = data['date']
		assign_date = change_dateformat(assign_date)
		vehicle_id = data['vehicle_id']
		staff_id = data['staff_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not VehiclesData.objects.filter(vehicle_id=vehicle_id, status='1').exists():
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
			elif not StaffData.objects.filter(staff_id=staff_id, status='1').exists():
				data={'msg':'Incorrect Staff ID'}
				return get_failure_response(data)
			elif not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			elif not CylinderData.objects.filter(business_id=business_id).exists():
				data={'msg':'Make Cylinder Purchase Entry First'}
				return get_failure_response(data)
			elif not VehiclesData.objects.filter(vehicle_id=vehicle_id, assign_id='N/A').exists():
				assign_id=VehiclesData.objects.filter(vehicle_id=vehicle_id)[0].assign_id
				assign_date_2=CylinderAssignData.objects.filter(assign_id=assign_id)[0].assign_date
				
				if assign_date_2 == assign_date:
					assign_filled_quantity=CylinderAssignData.objects.filter(assign_id=assign_id)[0].filled_quantity
					new_filled_quantity=int(filled_quantity)+int(assign_filled_quantity)
					CylinderAssignData.objects.filter(assign_id=assign_id).update(
						filled_quantity=new_filled_quantity
					)
					cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
					total_filled_cylinder=int(cylinder_data.total_filled_cylinder)-int(filled_quantity)
					total_cylinder=int(cylinder_data.total_cylinder)-int(filled_quantity)

					CylinderData.objects.filter(business_id=business_id).update(
						total_filled_cylinder=str(total_filled_cylinder),
						total_cylinder=str(total_cylinder)
					)
					data={'msg':'Cylinders Assigned!'}
					return get_success_response(data)
				else:
					data={'msg':'Vehicle Already Have An Assignment'}
					return get_failure_response(data)
			else:
				a="ASGN000"
				x=1
				aid=a+str(x)
				while CylinderAssignData.objects.filter(assign_id=aid).exists():
					x=x+1
					if x>=10:
						a='ASGN00'
					if x>=100:
						a='ASGN0'
					if x>=1000:
						a='ASGN'
					aid=a+str(x)
				x=int(x)
				
				CylinderAssignData(
					assign_id=aid,
					vehicle_id=vehicle_id,
					staff_id=staff_id,
					business_id=business_id,
					filled_quantity=str(filled_quantity),
					current_cylinder_cost=str(current_cylinder_cost),
					assign_date=assign_date
				).save()
				
				VehiclesData.objects.filter(vehicle_id=vehicle_id).update(assign_id=aid)
				
				cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
				total_filled_cylinder=int(cylinder_data.total_filled_cylinder)-int(filled_quantity)
				total_cylinder=int(cylinder_data.total_cylinder)-int(filled_quantity)

				CylinderData.objects.filter(business_id=business_id).update(
					total_filled_cylinder=str(total_filled_cylinder),
					total_cylinder=str(total_cylinder)
				)
				data={'msg':'Cylinders Assigned!'}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def cylinder_history(request):
	if request.method=='POST':
		data = request.data
		business_id = data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				return get_success_response(get_cylinder_history(business_id))
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def cylinder_dashboard(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				
				generate_daily_report(business_id, str(datetime.date.today()))
				
				total_profit = 0.0
				weekly_profit = 0.0
				total_sales = 0.0
				weekly_sales = 0.0
				yesterday_sales = 0.0
				cylinder_with_vehicles = 0
				yesterday_profit = 0.0
				report_data = CylinderDailyReportData.objects.filter(business_id=business_id)
				
				data={}
				for x in CylinderDailyReportData.objects.filter(business_id=business_id):
					total_profit = total_profit+float(x.profit)
					total_sales = total_sales+(float(x.total_cylinder_sold)*float(x.per_cylinder_cost))
					if not str(x.entry_date) == str(datetime.date.today()):
						yesterday_sales=float(x.total_cylinder_sold)*float(x.per_cylinder_cost)
						yesterday_profit=float(x.profit)
				
				if len(report_data) > 7:
					flag=0
					rlen=len(report_data)-6
					for x in report_data:
						if flag > rlen:
							weekly_profit = weekly_profit+float(x.profit)
							weekly_sales = weekly_sales+(float(x.total_cylinder_sold)*float(x.per_cylinder_cost))
						flag=flag+1

				#Total filled cylinders with vehicles
				for x in CylinderAssignData.objects.filter(business_id=business_id, completed='0'):
					cylinder_with_vehicles = cylinder_with_vehicles+int(x.filled_quantity)	
				
				try:
					cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
				except IndexError:
					CylinderData(business_id=business_id).save()
				
				cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
				
				data={
					'total_sales':total_sales,
					'weekly_sales':weekly_sales,
					'yesterday_sales':yesterday_sales,
					'total_profit':total_profit,
					'weekly_profit':weekly_profit,
					'yesterday_profit':str(yesterday_profit),
					'total_filled_cylinders':str(cylinder_data.total_filled_cylinder),
					'total_empty_cylinders':str(cylinder_data.total_empty_cylinder),
					'total_cylinders':str(cylinder_data.total_cylinder),
					'total_filled_cylinder_with_vehicles':cylinder_with_vehicles
				}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_assigned_vehicles_list_by_date(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		assign_date=data['assign_date']
		assign_date=change_dateformat(assign_date)
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				dic={}
				lt=[]
				for x in CylinderAssignData.objects.filter(business_id=business_id):
					if x.assign_date == assign_date:
						dic={
							'assign_id':x.assign_id,
							'assign_date':x.assign_date,
							'vehicle_id':x.vehicle_id,
							'staff_id':x.staff_id,
							'cylinder_assigned':x.filled_quantity,
							'cost_per_cylinder':x.current_cylinder_cost,
							'completed':x.completed
						}
						lt.append(dic)
				return get_success_response(lt)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_assignments_list(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				dic={}
				lt=[]
				for x in CylinderAssignData.objects.filter(business_id=business_id):
					dic={
						'assign_id':x.assign_id,
						'assign_date':x.assign_date,
						'vehicle_id':x.vehicle_id,
						'staff_id':x.staff_id,
						'cylinder_assigned':x.filled_quantity,
						'cost_per_cylinder':x.current_cylinder_cost,
						'completed':x.completed
					}
					lt.append(dic)
				return get_success_response(lt)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_assigned_data_by_date_and_vehicle_id(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		assign_date=data['assign_date']
		assign_date=change_dateformat(assign_date)
		vehicle_id=data['vehicle_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			elif not VehiclesData.objects.filter(vehicle_id=vehicle_id).exists():
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
			elif not VehiclesData.objects.filter(vehicle_id=vehicle_id, assign_id='N/A').exists():
				assign_id=VehiclesData.objects.filter(vehicle_id=vehicle_id)[0].assign_id
				dic={}
				for x in CylinderAssignData.objects.filter(business_id=business_id, completed='0'):
					if x.assign_date == assign_date:
						dic={
							'assign_id':x.assign_id,
							'staff_id':x.staff_id,
							'cylinder_assigned':x.filled_quantity,
							'cost_per_cylinder':x.current_cylinder_cost
						}
					else:
						dic={
							'assign_id':None,
							'staff_id':None,
							'cylinder_assigned':None,
							'cost_per_cylinder':None
						}
				return get_success_response(dic)
			else:
				data={'msg':'Vehicle has no incomplete assignment.'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def deassign_vehicle(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		assign_id=data['assign_id']
		filled_quantity_returned=int(data['filled_quantity_returned'])
		empty_quantity_returned=int(data['empty_quantity_returned'])
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			elif not CylinderAssignData.objects.filter(assign_id=assign_id).exists():
				data={'msg':'Incorrect Assign ID'}
				return get_failure_response(data)
			else:
				cyl_assgn=CylinderAssignData.objects.filter(assign_id=assign_id)[0]
				if (int(cyl_assgn.filled_quantity) < int(filled_quantity_returned)):
					data={'msg':'Qantity of filled cylinders returned is greater than the quantity of cylinder assigned.'}
					return get_failure_response(data)
				elif not (int(cyl_assgn.filled_quantity) == (int(filled_quantity_returned)+int(empty_quantity_returned))):
					data={'msg':"Sum of filled and empty cylinders returned doesn't match with the total cylinders assigned."}
					return get_failure_response(data)
				elif CylinderAssignData.objects.filter(assign_id=assign_id, completed='1').exists():
					data={'msg':"Assignment Already Deassigned"}
					return get_failure_response(data)
				else:
					CylinderAssignData.objects.filter(assign_id=assign_id).update(
						completed='1',
						filled_quantity_returned=str(filled_quantity_returned),
						empty_quantity_returned=str(empty_quantity_returned)
					)
					cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
					total_filled_cylinder = str(int(cylinder_data.total_filled_cylinder) + int(filled_quantity_returned))
					total_empty_cylinder = str(int(cylinder_data.total_empty_cylinder) + int(empty_quantity_returned))
					total_cylinder = str(int(total_filled_cylinder) + int(total_empty_cylinder))
					
					CylinderData.objects.filter(business_id=business_id).update(
						total_filled_cylinder=str(total_filled_cylinder),
						total_empty_cylinder=str(total_empty_cylinder),
						total_cylinder=str(total_cylinder)
					)
					
					vehicle_id=CylinderAssignData.objects.filter(assign_id=assign_id)[0].vehicle_id
					VehiclesData.objects.filter(vehicle_id=str(vehicle_id)).update(assign_id='N/A')
				return get_success_response({'msg':'Dessigned Successfully'})
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#Cylinder Daily Entry Report Entry
@api_view(['POST'])
@csrf_exempt
def generate_report(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		report_date=change_dateformat(data['report_date'])
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				try:
					cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
				except IndexError:
					data={'msg':'Purchase Entry Error : Make purchase entry first.'}
					return get_failure_response(data)
				a="RPRT000"
				x=1
				aid=a+str(x)
				while CylinderDailyReportData.objects.filter(report_id=aid).exists():
					x=x+1
					if x>=10:
						a='RPRT00'
					if x>=100:
						a='RPRT0'
					if x>=1000:
						a='RPRT'
					aid=a+str(x)
				x=int(x)
				

				average_sale_price = 0.0
				total_sale_price = 0.0
				number_of_sales = 0.0
				total_filled_cylinder_returned = 0
				total_empty_cylinder_returned = 0
				total_cylinder_assigned = 0
				total_cylinder_sold = 0

				
				for elt in CylinderAssignData.objects.filter(business_id=business_id, report_generated='0', completed='1'):
					if str(elt.created_date.date()) == report_date:
						total_sale_price = total_sale_price + float(elt.current_cylinder_cost)
						number_of_sales = number_of_sales + 1
						total_filled_cylinder_returned = total_filled_cylinder_returned + int(elt.filled_quantity_returned)
						total_empty_cylinder_returned = total_empty_cylinder_returned + int(elt.empty_quantity_returned)
						total_cylinder_sold = total_cylinder_sold + (int(elt.filled_quantity) - int(elt.filled_quantity_returned))
						CylinderAssignData.objects.filter(business_id=business_id, assign_id=elt.assign_id).update(report_generated='1')
				
				total_cylinder_assigned = total_filled_cylinder_returned + total_empty_cylinder_returned
				
				try:
					average_sale_price = total_sale_price/number_of_sales
				except ZeroDivisionError:
					average_sale_price = 0.0
				
				profit = calculate_profit(report_date, business_id)
				
				#CylinderDailyReportData.objects.all().delete()
				
				if CylinderDailyReportData.objects.filter(entry_date=report_date).exists():
					data={'msg':'ERROR : Entry Already Made'}
					return get_failure_response(data)
				
				CylinderDailyReportData(
					report_id=aid,
					business_id=business_id,
					entry_date=report_date,
					per_cylinder_cost=str(average_sale_price),
					profit=str(profit),
					total_filled_cylinder_returned=str(total_filled_cylinder_returned),
					total_empty_cylinder_returned=str(total_empty_cylinder_returned),
					total_cylinder_sold=str(total_cylinder_sold),
					total_cylinder_assigned=str(total_cylinder_assigned)
				).save()
				sales=total_cylinder_sold*average_sale_price
				cyl_daily=CylinderDailyReportData.objects.filter(report_id=aid)[0]
				data={
					'report_for_'+report_date:{
						'total_cylinder_sold':str(cyl_daily.total_cylinder_sold),
						'total_filled_cylinder_returned':str(cyl_daily.total_filled_cylinder_returned),
						'total_empty_cylinder_returned':str(cyl_daily.total_empty_cylinder_returned),
						'total_cylinder_assigned':str(cyl_daily.total_cylinder_assigned),
						'total_sales':str(sales),
						'total_profit':cyl_daily.profit,
						'msg':'Entry Made Successfully for the date : '+report_date
					},
					'godown_data':{
						'total_filled_cylinders':str(cylinder_data.total_filled_cylinder),
						'total_empty_cylindders':str(cylinder_data.total_empty_cylinder),
						'total_cylinders':str(cylinder_data.total_cylinder)
					}
				}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def check_vehicle_assignment(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		vehicle_id=data['vehicle_id']
		check_date = data['check_date']
		check_date = change_dateformat(check_date)
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			elif not VehiclesData.objects.filter(vehicle_id=vehicle_id).exists():
				data={'msg':'Incorrect Vehicle ID'}
				return get_failure_response(data)
			elif CylinderAssignData.objects.filter(vehicle_id=vehicle_id, assign_date=check_date, completed='0').exists():
				assign = CylinderAssignData.objects.filter(vehicle_id=vehicle_id, assign_date=check_date, completed='0')[0]
				data={
					'cylinder_assigned':True,
					'assign_id':str(assign.assign_id),
					'driver_id/staff_id':str(assign.staff_id),
					'filled_cylinder_quantity_assigned':str(assign.filled_quantity),
					'cylinder_cost_assigned':str(assign.current_cylinder_cost)
				}
				return get_success_response(data)
			else:
				data={'cylinder_assigned':False,'msg':'Cylinders not assigned to this vehicle on this date.'}
				return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_cylinder_count(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				if CylinderData.objects.filter(business_id=business_id).exists():
					cy_data=CylinderData.objects.filter(business_id=business_id)[0]
					data={
						'filled_cylinders':str(cy_data.total_filled_cylinder),
						"empty_cylinders":str(cy_data.total_empty_cylinder),
						'total_cylinders':str(cy_data.total_cylinder)
					}
					return get_success_response(data)
				else:
					data={'msg':'This business is not registered for cylinders.'}
					return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#Fuel Purchase Entry
@api_view(['POST'])
@csrf_exempt
def fuel_purchase_entry(request):
	if request.method=='POST':
		data=request.data
		business_id=str(data['business_id'])
		entry_date=change_dateformat(data['entry_date'])
		purchased_quantity=str(data['purchased_quantity'])
		price_per_liter=str(data['price_per_liter'])
		total_price=str(data['total_price'])
		fuel_type=str(data['fuel_type'])
		fuel_bill=data['fuel_bill']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				if fuel_type == '0':
					PetrolPurchaseData(
						bill_date=entry_date,
						bill_id=generate_bill_id(),
						business_id=business_id,
						purchased_quantity=purchased_quantity,
						price_per_liter=price_per_liter,
						total_price=total_price,
						bill=fuel_bill
					).save()
					if FuelData.objects.filter(business_id=business_id).exists():
						fuel_data=FuelData.objects.filter(business_id=business_id)[0]
						FuelData.objects.filter(business_id=business_id).update(
							current_petrol_quantity=str(float(fuel_data.current_petrol_quantity)+float(purchased_quantity))
						)
					else:
						if len(FuelData.objects.all()) < 2:
							FuelData(
								business_id=business_id,
								current_petrol_quantity=purchased_quantity
							).save()
						else:
							PetrolPurchaseData.objects.filter(business_id=business_id).delete()
							data={'msg':'A business is already registered.'}
							return get_success_response(data)
					data={'msg':'Petrol Purchase Entry Made Successfully'}
					return get_success_response(data)
				elif fuel_type == '1':
					DieselPurchaseData(
						bill_date=entry_date,
						bill_id=generate_bill_id(),
						business_id=business_id,
						purchased_quantity=purchased_quantity,
						price_per_liter=price_per_liter,
						total_price=total_price,
						bill=fuel_bill
					).save()
					if FuelData.objects.filter(business_id=business_id).exists():
						fuel_data=FuelData.objects.filter(business_id=business_id)[0]
						FuelData.objects.filter(business_id=business_id).update(
							current_diesel_quantity=str(float(fuel_data.current_diesel_quantity)+float(purchased_quantity))
						)
					else:
						if len(FuelData.objects.all()) < 2:
							FuelData(
								business_id=business_id,
								current_diesel_quantity=purchased_quantity
							).save()
						else:
							DieselPurchaseData.objects.filter(business_id=business_id).delete()
							data={'msg':'A business is already registered.'}
							return get_success_response(data)

					data={'msg':'Diesel Purchase Entry Made Successfully'}
					return get_success_response(data)
				else:
					data={'msg':'Incorrect Fuel Type'}
					return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#Petrol Sales Entry
@api_view(['POST'])
@csrf_exempt
def petrol(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		entry_date=change_dateformat(data['entry_date'])
		entry_time=data['entry_time']
		quantity=data['quantity']
		price_per_liter=data['price_per_liter']
		total_price=str(float(quantity)*float(price_per_liter))
		meter_pic=data['meter_pic']
		machine_type=data['machine_type']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				if FuelData.objects.filter(business_id=business_id).exists():
					fuel_data=FuelData.objects.filter(business_id=business_id)[0]
					if float(fuel_data.current_petrol_quantity) <= 0:
						data={'msg':'Empty Petrol'}
						return get_success_response(data)
					else:
						FuelData.objects.filter(business_id=business_id).update(
							current_petrol_quantity=str(float(fuel_data.current_petrol_quantity)-float(quantity))
						)
						bill_id=generate_bill_id()
						PetrolBillData(
							bill_date=entry_date,
							bill_time=entry_time,
							bill_id=bill_id,
							business_id=business_id,
							quantity=quantity,
							price_per_liter=price_per_liter,
							total_price=total_price,
							machine_type=machine_type
						).save()
						PetrolBillPic(
							bill_id=bill_id,
							meter_pic=meter_pic
						).save()
						data={'msg':'Petrol Bill Added Successfully'}
						return get_success_response(data)
				else:
					data={'msg':'Petrol Purchase Entry Not Made Yet'}
					return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def petrol_bills(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				data={'bills':get_petrol_bills(business_id)}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

#Diesel Sales Entry
@api_view(['POST'])
@csrf_exempt
def diesel(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		entry_date=change_dateformat(data['entry_date'])
		entry_time=data['entry_time']
		quantity=data['quantity']
		price_per_liter=data['price_per_liter']
		meter_pic=data['meter_pic']
		machine_type=data['machine_type']
		total_price=str(float(quantity)*float(price_per_liter))
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				if FuelData.objects.filter(business_id=business_id).exists():
					fuel_data=FuelData.objects.filter(business_id=business_id)[0]
					if float(fuel_data.current_diesel_quantity) <= 0:
						data={'msg':'Empty Diesel'}
						return get_success_response(data)
					else:
						FuelData.objects.filter(business_id=business_id).update(
							current_diesel_quantity=str(float(fuel_data.current_diesel_quantity)-float(quantity))
						)
						bill_id=generate_bill_id()
						DieselBillData(
							bill_date=entry_date,
							bill_time=entry_time,
							bill_id=bill_id,
							business_id=business_id,
							quantity=quantity,
							price_per_liter=price_per_liter,
							total_price=total_price,
							machine_type=machine_type
						).save()
						DieselBillPic(
							bill_id=bill_id,
							meter_pic=meter_pic
						).save()
						data={'msg':'Diesel Bill Added Successfully'}
						return get_success_response(data)
				else:
					data={'msg':'Diesel sPurchase Entry Not Made Yet'}
					return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def diesel_bills(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				data={'msg':'Incorrect Business ID'}
				return get_failure_response(data)
			else:
				data={'bills':get_diesel_bills(business_id)}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def fuel_dashboard(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				return get_success_response(get_fuel_dashboard(business_id))
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_current_petrol_quantity(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				if FuelData.objects.filter(business_id=business_id).exists():
					petrol=FuelData.objects.filter(business_id=business_id)[0].current_petrol_quantity
					data={'current_petrol_quantity':petrol}
					return get_success_response(data)
				else:
					data={'msg':'This business is not yet registered in fuel category.'}
					return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def get_current_diesel_quantity(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				if FuelData.objects.filter(business_id=business_id).exists():
					diesel=FuelData.objects.filter(business_id=business_id)[0].current_diesel_quantity
					data={'current_diesel_quantity':diesel}
					return get_success_response(data)
				else:
					data={'msg':'This business is not yet registered in fuel category.'}
					return get_failure_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def calculate_fuel_profit_of_day(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		entry_date=change_dateformat(data['entry_date'])
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				total_petrol_price = 0.0
				total_diesel_price = 0.0
				total_petrol_sold = 0.0
				total_diesel_sold = 0.0
				petrol_purchase_price = 0.0
				diesel_purchase_price = 0.0
				
				for x in PetrolBillData.objects.filter(business_id=business_id, bill_date=entry_date):
					total_petrol_sold = total_petrol_sold+float(x.quantity)
					total_petrol_price=total_petrol_price+float(x.total_price)
				
				for x in DieselBillData.objects.filter(business_id=business_id, bill_date=entry_date):
					total_diesel_sold = total_diesel_sold+float(x.quantity)
					total_diesel_price=total_diesel_price+float(x.total_price)
				
				for x in PetrolPurchaseData.objects.filter(business_id=business_id):
					petrol_purchase_price = float(x.price_per_liter)
				
				for x in DieselPurchaseData.objects.filter(business_id=business_id):
					diesel_purchase_price = float(x.price_per_liter)
				
				total_petrol_purchase_price=total_petrol_sold*petrol_purchase_price
				total_diesel_purchase_price=total_diesel_sold*diesel_purchase_price

				petrol_profit = total_petrol_price - total_petrol_purchase_price
				diesel_profit = total_diesel_price - total_diesel_purchase_price
				total_profit = petrol_profit + diesel_profit
				
				if FuelDailyData.objects.filter(entry_date=entry_date, business_id=business_id).exists():
					FuelDailyData.objects.filter(entry_date=entry_date, business_id=business_id).update(
						diesel_profit=diesel_profit,
						petrol_profit=petrol_profit,
						total_profit=total_profit
					)
				else:
					a="ENTRY"
					x=1
					aid=a+str(x)
					while FuelDailyData.objects.filter(entry_id=aid).exists():
						x=x+1
						aid=a+str(x)
					x=int(x)
					FuelDailyData(
						business_id=business_id,
						entry_id=aid,
						entry_date=entry_date,
						diesel_profit=diesel_profit,
						petrol_profit=petrol_profit,
						total_profit=total_profit
					).save()

				data={
					'msg':'Profit for '+entry_date,
					'petrol_profit':str(petrol_profit),
					'diesel_profit':str(diesel_profit),
					'total_profit':str(total_profit)
				}

				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def savemeterreadings(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		photo=data['photo']
		fuel_type=data['fuel_type']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				MeterReadingData(
					business_id=business_id,
					photo=photo,
					fuel_type=fuel_type
				).save()
				data={'msg':'Meter Reading Saved Successfully.'}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def listmeterreadings(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				lt=[]
				dic={}
				for x in MeterReadingData.objects.filter(business_id=business_id):
					dic={
					'datetime':x.created_date,
					'photo':x.photo.url,
					'fuel_type':x.fuel_type
					}
					lt.append(dic)
				data={'readings':lt}
				return get_success_response(data)
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def cylinder_sales_report(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				response = HttpResponse()
				response['Content-Disposition'] = 'attachment;filename=Cylinder_Sales_Report.csv'
				writer = csv.writer(response)
				writer.writerow(['Date', 'Sales of the Day', 'Profit of the Day'])
				for x in CylinderDailyReportData.objects.filter(business_id=business_id):
					writer.writerow([x.entry_date, str(float(x.total_cylinder_sold)*float(x.per_cylinder_cost)), x.profit])
				return response
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

@api_view(['POST'])
@csrf_exempt
def cylinder_purchase_report(request):
	if request.method=='POST':
		data=request.data
		business_id=data['business_id']
		Authorization = request.META.get('HTTP_TOKEN')
		if check_admin_authorization(Authorization) or check_staff_authorization(Authorization):
			if not BusinessData.objects.filter(business_id=business_id).exists():
				return get_failure_response({'msg':'Incorrect Business ID'})
			else:
				response = HttpResponse()
				response['Content-Disposition'] = 'attachment;filename=Cylinder_Purchase_Report.csv'
				writer = csv.writer(response)
				writer.writerow(['Date', 'Quantity Purchased', 'Price Per Cylinder', 'Total Amount'])
				for x in CylinderPurchaseData.objects.filter(business_id=business_id):
					writer.writerow([x.created_date.date(), x.quantity, x.per_cylinder_price, x.total_price])
				return response
		else:
			return get_auth_token_error()
	else:
		data={'msg':'ERROR404'}
		return get_failure_response(data)

def fuel_sales_report(request):
	if request.method=='GET':
		business_id=request.GET.get('business_id')
		fuel_type=int(request.GET.get('fuel_type'))
		if not BusinessData.objects.filter(business_id=business_id).exists():
			return HttpResponse('Incorrect Business ID')
		else:
			columns = ['Type', 'Date', 'Total Sales', 'Total Profit']
			data = get_fuel_sales(business_id, fuel_type)
			
			df = pd.DataFrame(data, columns=columns)
			df.to_excel('Fuel_Sales_Records.xlsx')
			
			filename = 'Fuel_Sales_Records.xlsx'
			fl_path = filename
			file_path = filename
			file_wrapper = FileWrapper(open(filename, 'rb'))
			file_mimetype, _ = mimetypes.guess_type(file_path)
			response = HttpResponse(file_wrapper, content_type=file_mimetype )
			response['X-Sendfile'] = file_path
			response['Content-Length'] = os.stat(file_path).st_size
			response['Content-Disposition'] = 'attachment; filename=%s' % file_path
			os.remove(filename)
			return response
	else:
		return HttpResponse('ERROR404 : Invalid Request Type')

def fuel_purchase_report(request):
	if request.method=='GET':
		business_id=request.GET.get('business_id')
		fuel_type=int(request.GET.get('fuel_type'))
		if not BusinessData.objects.filter(business_id=business_id).exists():
			return HttpResponse('Incorrect Business ID')
		else:
			data=[]
			
			columns = ['Type', 'Date', 'Purchased Quantity', 'Price', 'Total Price']
			
			if fuel_type == 0:
				for x in PetrolPurchaseData.objects.filter(business_id=business_id):
					data.append(['Petrol', x.bill_date, x.purchased_quantity, x.price_per_liter, x.total_price])
			elif fuel_type == 1:
				for x in DieselPurchaseData.objects.filter(business_id=business_id):
					data.append(['Diesel', x.bill_date, x.purchased_quantity, x.price_per_liter, x.total_price])
			
			df = pd.DataFrame(data, columns=columns)
			df.to_excel('Fuel_Purchase_Records.xlsx')
			
			filename = 'Fuel_Purchase_Records.xlsx'
			fl_path = filename
			file_path = filename
			file_wrapper = FileWrapper(open(filename, 'rb'))
			file_mimetype, _ = mimetypes.guess_type(file_path)
			response = HttpResponse(file_wrapper, content_type=file_mimetype )
			response['X-Sendfile'] = file_path
			response['Content-Length'] = os.stat(file_path).st_size
			response['Content-Disposition'] = 'attachment; filename=%s' % file_path
			os.remove(filename)
			return response
	else:
		return HttpResponse('ERROR404 : Invalid Request Type')

def trial(request):
	data=[]
	for x in PetrolPurchaseData.objects.filter(business_id='B003'):
		data.append(['Petrol', x.bill_date, x.purchased_quantity, x.price_per_liter, x.total_price])
	df = pd.DataFrame(data, columns=['Type', 'Date', 'Purchased Quantity', 'Price', 'Total Price'])
	df.to_excel('Test.xlsx')
	return HttpResponse('Done!')

def cleardb(request):
	#AdminData.objects.all().delete()
	#VehiclesData.objects.all().update(assign_id='N/A')
	#StaffData.objects.all().delete()
	#CylinderPurchaseData.objects.all().delete()
	#CylinderAssignData.objects.all().delete()
	#CylinderDailyReportData.objects.all().delete()
	#CylinderData.objects.all().delete()
	#CylinderDailyReportData.objects.all().delete()
	PetrolBillData.objects.all().update(machine_type='1')
	DieselBillData.objects.all().update(machine_type='1')
	#DieselPurchaseData.objects.all().delete()
	#PetrolPurchaseData.objects.all().delete()
	#FuelDailyData.objects.all().delete()
	#FuelData.objects.all().delete()
	#MeterReadingData.objects.all().delete()
	#BusinessData.objects.filter(business_id='B004').delete()
	return HttpResponse('Done!')