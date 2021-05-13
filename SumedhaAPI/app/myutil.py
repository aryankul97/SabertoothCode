from app.models import *
import uuid
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.models import *
import datetime
import requests

def change_dateformat(assign_date):
	date_str=assign_date.replace('/', '')
	month=int(date_str[0:2])
	day=int(date_str[2:4])
	year=int('20'+date_str[4:6])
	assign_date=str(datetime.date(year, month, day))
	return str(assign_date)

def get_internal_error():
	data={'msg':'Internal Error'}
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def get_auth_token_error():
	data={'msg':'Incorrect Authorization Token'}
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def get_staff_authorization(staffid):
	authorization=str(uuid.uuid5(uuid.NAMESPACE_DNS, staffid))
	return authorization

def get_admin_authorization(admin_id):
	Authorization=str(uuid.uuid5(uuid.NAMESPACE_DNS, admin_id))
	return Authorization

def check_admin_authorization(Authorization):
	for x in AdminData.objects.all():
		if get_admin_authorization(x.admin_id) == Authorization:
			return True
	return False

def check_staff_type(staff_type_id):
	stafftype=StaffTypeData.objects.filter(staff_type_id=staff_type_id)[0]
	if stafftype.staff_type_name == 'MANAGER':
		return True
	else:
		return False

def check_staff_authorization(authorization):
	staff=StaffData.objects.all()
	for x in staff:
		if get_staff_authorization(x.staff_id) == authorization:
			return True
	return False

def get_user_id_from_Authorization(Authorization):
	users=UserData.objects.all()
	for x in users:
		if get_userid_Authorization(x.user_id) == Authorization:
			return x.user_id

def get_success_response(data):
	dic={'status':True, 'status_code':1000, 'data':data}
	return Response(dic)

def get_failure_response(data):
	dic={'status':False, 'status_code':999, 'data':data}
	return Response(dic)

def get_vehicles_list(business_id):
	vehicles = VehiclesData.objects.filter(business_id=business_id, status='1')
	dic = {}
	lt = []
	for x in vehicles:
		dic={
			'vehicle_id':x.vehicle_id,
			'business_id':x.business_id,
			'assign_id':x.assign_id,
			'staff_id':x.staff_id,
			'number_plate':x.number_plate,
			'vehicle_name':x.vehicle_name,
			'driver_assigned':x.driver_assigned,
			'driver_name':x.driver_name,
			'manufacturer':x.manufacturer,
			'hazardous_license_expiry_date':x.hazardous_license_expiry_date,
			'insurence_expiry_date':x.insurence_expiry_date,
			'vehicle_photo':x.vehicle_photo.url,
			'rc_number':x.rc_number.url,
			'insurence_number':x.insurence_number.url,
			'puc':x.puc.url
		}
		lt.append(dic)
	return lt

def get_staff_data(business_id):
	staff = StaffData.objects.filter(business_id=business_id, staff_type_id='ST001', status='1')
	dic = {}
	lt = []
	for x in staff:
		dic={
			'staff_id':x.staff_id,
			'business_id':x.business_id,
			'staff_type_id':x.staff_type_id,
			'fullname':x.fullname,
			'username':x.username,
			'password':x.password,
			'mobile':x.mobile,
			'alternate_mobile':x.alternate_mobile,
			'dob':x.dob,
			'aadhar':x.aadhar
		}
		try:
			dic.update({
				'profile_picture':x.profile_picture.url,
				'driving_license':x.driving_license.url
			})
		except:
			dic.update({
				'profile_picture':None,
				'driving_license':None
			})
		lt.append(dic)
	return lt

def get_cylinder_bills(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	dic = {}
	lt = []
	for x in bills:
		dic={
			'bill_id':x.bill_id,
			'business_id':x.business_id,
			'quantity':x.quantity,
			'empty_cylinder_sent':x.empty_cylinder_sent,
			'paymode':x.paymode,
			'total_price':x.total_price,
			'bill_date':x.bill_date,
			'bill':x.bill.url
		}
		lt.append(dic)
	return lt

def get_cylinder_sales_total(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	total=0.0
	for x in bills:
		total=total+float(x.total_price)
	return total

def get_cylinder_today_sales_total(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	total=0.0
	todaydate=str(datetime.date.today())
	for x in bills:
		if todaydate == x.bill_date:
			total=total+float(x.total_price)
	return total

def get_total_cylinder(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	total=0
	for x in bills:
		total=total+int(x.quantity)
		total=total+int(x.empty_cylinder_sent)
	return total

def get_filled_cylinder(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	total=0
	for x in bills:
		total=total+int(x.quantity)
	return total

def get_empty_cylinder(business_id):
	bills = CylinderPurchaseData.objects.filter(business_id=business_id)
	total=0
	for x in bills:
		total=total+int(x.empty_cylinder_sent)
	return total

def get_cylinder_sales_from_util(business_id):
	dic={
		'total':get_cylinder_sales_total(business_id),
		'today_total':get_cylinder_today_sales_total(business_id),
		'total_cylinder':get_total_cylinder(business_id),
		'filled_cylinder':get_filled_cylinder(business_id),
		'empty_cylinder':get_empty_cylinder(business_id)
	}
	return dic

def get_business_data():
	business = BusinessData.objects.all()
	dic = {}
	lt = []
	for x in business:
		dic={
			'business_id':x.business_id,
			'business_name':x.business_name,
			'business_pic':x.business_picture.url
		}
		lt.append(dic)
	return lt

def get_role_id():
	x=0
	while StaffTypeData.objects.filter(role_id=str(x)).exists():
		x=x+1
	return str(x)

def sendOTP(mobile, otp):
	msg='Hi there! Your OTP Verification Code is '+str(otp)
	param={
	  "sender": "SABTEC",
	  "route": "4",
	  "country": "91",
	  "unicode": "1",
	  "sms": [
	    {
	      "message": msg,
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
		return get_failure_response

def get_petrol_bills(business_id):
	dic={}
	lt=[]
	for x in PetrolBillData.objects.filter(business_id=business_id):
		meter_pic=None
		if PetrolBillPic.objects.filter(bill_id=x.bill_id).exists():
			meter_pic=PetrolBillPic.objects.filter(bill_id=x.bill_id)[0].meter_pic.url
		dic={
		'date':x.bill_date,
		'time':x.bill_time,
		'bill_id':x.bill_id,
		'quantity':x.quantity,
		'price_per_liter':x.price_per_liter,
		'total_price':x.total_price,
		'machine_type':x.machine_type,
		'meter_pic':meter_pic
		}
		lt.append(dic)
	return list(reversed(lt))

def get_diesel_bills(business_id):
	dic={}
	lt=[]
	for x in DieselBillData.objects.filter(business_id=business_id):
		meter_pic=None
		if DieselBillPic.objects.filter(bill_id=x.bill_id).exists():
			meter_pic=DieselBillPic.objects.filter(bill_id=x.bill_id)[0].meter_pic.url
		dic={
		'date':x.bill_date,
		'time':x.bill_time,
		'bill_id':x.bill_id,
		'quantity':x.quantity,
		'price_per_liter':x.price_per_liter,
		'total_price':x.total_price,
		'machine_type':x.machine_type,
		'meter_pic':meter_pic
		}
		lt.append(dic)
	return list(reversed(lt))

def get_total_petrol_quantity(business_id):
	total_petrol_quantity=0.0
	for x in PetrolBillData.objects.filter(business_id=business_id):
		total_petrol_quantity=total_petrol_quantity+float(x.quantity)
	return total_petrol_quantity

def get_fuel_sales(business_id, fuel_type):
	dates=[]
	data=[]
	total_petrol_sales=0.0
	total_diesel_sales=0.0
	if fuel_type == 0:
		for x in PetrolBillData.objects.filter(business_id=business_id):
			dates.append(x.bill_date)
		dates=set(dates)
		for d in dates:
			for x in PetrolBillData.objects.filter(business_id=business_id, bill_date=d):
				total_petrol_sales=total_petrol_sales+float(x.quantity)
			try:
				f_data=FuelDailyData.objects.filter(business_id=business_id, entry_date=d)[0]
				data.append(['Petrol', d, total_petrol_sales, f_data.petrol_profit])
			except:
				data.append(['Petrol', d, total_petrol_sales, None])
	elif fuel_type == 1:
		for x in DieselBillData.objects.filter(business_id=business_id):
			dates.append(x.bill_date)
		dates=set(dates)
		for d in dates:
			for x in DieselBillData.objects.filter(business_id=business_id):
				total_diesel_sales=total_diesel_sales+float(x.quantity)
			try:
				f_data=FuelDailyData.objects.filter(business_id=business_id, entry_date=d)[0]
				data.append(['Diesel', d, total_diesel_sales, f_data.diesel_profit])
			except:
				data.append(['Diesel', d, total_diesel_sales, None])
	return data

def get_average_petrol_price(business_id):
	total_price=0.0
	for x in PetrolBillData.objects.filter(business_id=business_id):
		total_price=float(x.price_per_liter)
	return total_price

def get_average_diesel_price(business_id):
	total_price=0.0
	for x in DieselBillData.objects.filter(business_id=business_id):
		total_price=float(x.price_per_liter)
	return total_price

def get_total_diesel_quantity(business_id):
	total_diesel_quantity=0.0
	for x in DieselBillData.objects.filter(business_id=business_id):
		total_diesel_quantity=total_diesel_quantity+float(x.quantity)
	return total_diesel_quantity

def get_total_petrol_price(business_id):
	total_price=0.0
	for x in PetrolBillData.objects.filter(business_id=business_id):
		total_price=total_price+float(x.total_price)
	return total_price

def get_total_diesel_price(business_id):
	total_price=0.0
	for x in DieselBillData.objects.filter(business_id=business_id):
		total_price=total_price+float(x.total_price)
	return total_price

def get_petrol_machine_stats(business_id):
	machines=['1','2','3','4']
	data=[]
	for machine in machines:
		amount=0.0
		dic={}
		for x in PetrolBillData.objects.filter(business_id=business_id, machine_type=machine):
			amount=amount+float(x.total_price)
		dic={'machine_name':machine, 'sales_amount':amount}
		data.append(dic)
	return data

def get_diesel_machine_stats(business_id):
	machines=['1','2','3','4']
	data=[]
	for machine in machines:
		amount=0.0
		dic={}
		for x in DieselBillData.objects.filter(business_id=business_id, machine_type=machine):
			amount=amount+float(x.total_price)
		dic={'machine_name':machine, 'sales_amount':amount}
		data.append(dic)
	return data

def get_fuel_dashboard(business_id):
	if FuelData.objects.filter(business_id=business_id).exists():
		fuel_data=FuelData.objects.filter(business_id=business_id)[0]
		dic={
			'total_petrol_sold_quantity':get_total_petrol_quantity(business_id),
			'total_diesel_sold_quantity':get_total_diesel_quantity(business_id),
			'average_petrol_price':get_average_petrol_price(business_id),
			'average_diesel_price':get_average_diesel_price(business_id),
			'total_petrol_collection':get_total_petrol_price(business_id),
			'total_diesel_collection':get_total_diesel_price(business_id),
			'petrol_sales_bills':get_petrol_bills(business_id),
			'diesel_sales_bills':get_diesel_bills(business_id),
			'current_diesel_quantity':str(fuel_data.current_diesel_quantity),
			'current_petrol_quantity':str(fuel_data.current_petrol_quantity),
			'petrol_machine_data':get_petrol_machine_stats(business_id),
			'diesel_machine_data':get_diesel_machine_stats(business_id),
		}
		return dic
	else:
		dic={
			'total_petrol_sold_quantity':'0',
			'total_diesel_sold_quantity':'0',
			'average_petrol_price':'0',
			'average_diesel_price':'0',
			'total_petrol_collection':'0',
			'total_diesel_collection':'0',
			'petrol_sales_bills':'Nil',
			'diesel_sales_bills':'Nil',
			'current_diesel_quantity':'0',
			'current_petrol_quantity':'0',
		}
		return dic

def generate_bill_id():
	b="BIL"
	x=1
	bid=b+str(x)
	while PetrolBillData.objects.filter(bill_id=bid).exists() or DieselBillData.objects.filter(bill_id=bid).exists() or CylinderPurchaseData.objects.filter(bill_id=bid).exists() or PetrolPurchaseData.objects.filter(bill_id=bid).exists() or DieselPurchaseData.objects.filter(bill_id=bid).exists():
		x=x+1
		bid=b+str(x)
	x=int(x)
	return bid

def get_cylinder_history(business_id):
	vehicles=VehiclesData.objects.filter(business_id=business_id, driver_assigned='1')
	dic={}
	lt=[]
	for x in vehicles:
		dic={
			'number_plate':x.number_plate,
			'vehicle_id':x.vehicle_id,
			'driver_name':x.driver_name
		}
		if CylinderAssignData.objects.filter(assign_id=x.assign_id).exists():
			for y in CylinderAssignData.objects.filter(assign_id=x.assign_id):
				dic.update({
					'assign_date':y.created_date.date(),
					'cost_per_cylinder':y.current_cylinder_cost,
					'total_cylinders':y.filled_quantity,
					'completed':y.completed
					})
			lt.append(dic)
		else:
			dic.update({
				'assign_date':'Not Assigned',
				'cost_per_cylinder':'Not Assigned',
				'total_cylinders':'Not Assigned'
			})
			lt.append(dic)
	return group_cylinder_history(lt)

def group_cylinder_history(history):
	data=[]
	dic={}
	for x in history:
		data.append(x['assign_date'])
	for x in data:
		lt=[]
		for y in history:
			if y['assign_date'] == x:
				lt.append(y)
			dic[str(x)] = lt
	return dic

def deassign_vehicles(today_date):
	for elt in CylinderAssignData2.objects.filter(created_date=today_date):
		VehiclesData.objects.filter(assign_id=elt.assign_id).update(assign_id='N/A')

def calculate_profit(report_date, business_id):
	sell_price = 0.0
	cost_price = 0.0
	cost = 0.0
	for price in CylinderPurchaseData.objects.filter(business_id=business_id):
		cost = float(price.per_cylinder_price)
	for elt2 in CylinderAssignData.objects.filter(business_id=business_id, assign_date=report_date, completed="1"):
		sell_price = sell_price+(float(elt2.current_cylinder_cost)*(float(elt2.filled_quantity)-float(elt2.filled_quantity_returned)))
		cost_price = cost_price+(float(cost)*(float(elt2.filled_quantity)-float(elt2.filled_quantity_returned)))
	return sell_price-cost_price

def generate_daily_report(business_id, report_date):
	try:
		cylinder_data = CylinderData.objects.filter(business_id=business_id)[0]
	except IndexError:
		data={
			'godown_data':{
				'total_filled_cylinders':0,
				'total_empty_cylindders':0,
				'total_cylinders':0
			}
		}
		return data
	#CylinderDailyReportData.objects.all().delete()
	a="RPRT"
	x=1
	aid=a+str(x)
	while CylinderDailyReportData.objects.filter(report_id=aid).exists():
		x=x+1
		aid=a+str(x)
	x=int(x)
				

	average_sale_price = 0.0
	total_sale_price = 0.0
	number_of_sales = 0
	total_filled_cylinder_returned = 0
	total_empty_cylinder_returned = 0
	total_cylinder_assigned = 0
	total_cylinder_sold = 0
	
	profit = calculate_profit(report_date, business_id)
	
	#CylinderAssignData.objects.all().update(report_generated='0')

	#assign_date=report_date, 
	for elt in CylinderAssignData.objects.filter(business_id=business_id, assign_date=report_date, report_generated='0', completed='1'):
		
		total_sale_price = total_sale_price + float(elt.current_cylinder_cost)
		
		number_of_sales = number_of_sales + 1
		total_filled_cylinder_returned = total_filled_cylinder_returned + int(elt.filled_quantity_returned)
		total_empty_cylinder_returned = total_empty_cylinder_returned + int(elt.empty_quantity_returned)
		total_cylinder_sold = total_cylinder_sold + (int(elt.filled_quantity) - int(elt.filled_quantity_returned))
		CylinderAssignData.objects.filter(business_id=business_id, assign_id=elt.assign_id).update(report_generated='1')
	
	total_cylinder_assigned = total_filled_cylinder_returned + total_empty_cylinder_returned
	#return total_cylinder_sold
	try:
		average_sale_price = total_sale_price/number_of_sales
	except ZeroDivisionError:
		average_sale_price = 0.0
	
	#CylinderDailyReportData.objects.all().delete()
				
	if CylinderDailyReportData.objects.filter(entry_date=report_date, business_id=business_id).exists():
		cd=CylinderDailyReportData.objects.filter(entry_date=report_date, business_id=business_id)
		
		per_cylinder_cost_=average_sale_price
		profit_=profit
		total_filled_cylinder_returned_=total_filled_cylinder_returned
		total_empty_cylinder_returned_=total_empty_cylinder_returned
		total_cylinder_sold_=total_cylinder_sold
		total_cylinder_assigned_=total_cylinder_assigned
		
		for x in cd:
			per_cylinder_cost_=per_cylinder_cost_+float(x.per_cylinder_cost)
			total_filled_cylinder_returned_=total_filled_cylinder_returned_+float(x.total_filled_cylinder_returned)
			total_empty_cylinder_returned_=total_empty_cylinder_returned_+float(x.total_empty_cylinder_returned)
			total_cylinder_sold_=total_cylinder_sold_+float(x.total_cylinder_sold)
			total_cylinder_assigned_=total_cylinder_assigned_+float(x.total_cylinder_assigned)

		CylinderDailyReportData.objects.filter(entry_date=report_date, business_id=business_id).update(
			per_cylinder_cost=str(per_cylinder_cost_),
			profit=str(profit_),
			total_filled_cylinder_returned=str(total_filled_cylinder_returned_),
			total_empty_cylinder_returned=str(total_empty_cylinder_returned_),
			total_cylinder_sold=str(total_cylinder_sold_),
			total_cylinder_assigned=str(total_cylinder_assigned_)
		)
	else:
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
	cyl_daily=CylinderDailyReportData.objects.filter(entry_date=report_date, business_id=business_id)[0]
	data={
		'godown_data':{
			'total_filled_cylinders':str(cylinder_data.total_filled_cylinder),
			'total_empty_cylindders':str(cylinder_data.total_empty_cylinder),
			'total_cylinders':str(cylinder_data.total_cylinder)
		}
	}
	return data