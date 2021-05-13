from django.db import models
from datetime import date
from django.conf import settings
from django.forms import DateField

class AdminData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	admin_id=models.CharField(max_length=50, primary_key=True)
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=50)
	mobile=models.CharField(max_length=15, default='NA')
	status=models.CharField(max_length=5, default='1')
	class Meta:
		db_table="AdminData"

class BusinessData(models.Model):
	business_id=models.CharField(max_length=50, primary_key=True)
	business_name=models.CharField(max_length=100)
	business_picture=models.FileField(upload_to='businesspic/', default='NA')
	class Meta:
		db_table="BusinessData"

class StaffTypeData(models.Model):
	staff_type_id=models.CharField(max_length=50, primary_key=True)
	staff_type_name=models.CharField(max_length=100)
	role_id=models.CharField(max_length=10, default='NA')
	class Meta:
		db_table="StaffTypeData"

class StaffData(models.Model):
	staff_id = models.CharField(max_length=50, primary_key=True)
	business_id = models.CharField(max_length=50)
	staff_type_id = models.CharField(max_length=50)
	fullname = models.CharField(max_length=100)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	mobile = models.CharField(max_length=15)
	alternate_mobile = models.CharField(max_length=15)
	dob = models.CharField(max_length=20)
	aadhar = models.CharField(max_length=20)
	profile_picture=models.FileField(upload_to='staffprofilepicture/', default='NA')
	driving_license=models.FileField(upload_to='drivinglicense/', default='NA')
	status = models.CharField(max_length=5, default='1')
	class Meta:
		db_table = "StaffData"

class VehiclesData(models.Model):
	vehicle_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	staff_id=models.CharField(max_length=50, default='N/A')
	assign_id=models.CharField(max_length=50, default='N/A')
	number_plate=models.CharField(max_length=100)
	vehicle_name=models.CharField(max_length=100)
	driver_assigned=models.CharField(max_length=5, default='0')
	driver_name=models.CharField(max_length=100, default='N/A')
	manufacturer=models.CharField(max_length=50)
	hazardous_license_expiry_date=models.CharField(max_length=50)
	insurence_expiry_date=models.CharField(max_length=50)
	vehicle_photo=models.FileField(upload_to='vehicles/', default='Not Availiable')
	rc_number=models.FileField(upload_to='vehicle_rc/', default='Not Availiable')
	insurence_number=models.FileField(upload_to='vehicle_insurence/', default='Not Availiable')
	puc=models.FileField(upload_to='vehicle_puc/', default='Not Availiable')
	status=models.CharField(max_length=5, default='1')
	class Meta:
		db_table = "VehiclesData"

class CylinderData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	business_id=models.CharField(max_length=50)
	total_filled_cylinder=models.CharField(max_length=50, default='1000')
	total_empty_cylinder=models.CharField(max_length=50, default='1000')
	total_cylinder=models.CharField(max_length=50, default='2000')
	class Meta:
		db_table = "CylinderData"

class CylinderPurchaseData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
	slot_quantity=models.CharField(max_length=50, default='0')
	empty_cylinder_sent=models.CharField(max_length=50)#Empty Cylinder Sent From Godown
	paymode=models.CharField(max_length=5, default='1')
	per_cylinder_price=models.CharField(max_length=50, default='0')
	total_price=models.CharField(max_length=50)
	bill_date=models.CharField(max_length=50)
	bill=models.FileField(upload_to='cylinderbills/', default='Not Availiable')
	class Meta:
		db_table = "CylinderPurchaseData"

class CylinderAssignData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	assign_id=models.CharField(max_length=50, primary_key=True)
	vehicle_id=models.CharField(max_length=50)
	staff_id=models.CharField(max_length=50)
	business_id=models.CharField(max_length=50)
	filled_quantity=models.CharField(max_length=50)#Quantity of filled cylinder assigned
	current_cylinder_cost=models.CharField(max_length=50)
	assign_date=models.CharField(max_length=50)
	filled_quantity_returned=models.CharField(max_length=50, default='0')
	empty_quantity_returned=models.CharField(max_length=50, default='0')
	completed=models.CharField(max_length=4, default='0')
	report_generated=models.CharField(max_length=4, default='0')
	class Meta:
		db_table = "CylinderAssignData"

class CylinderAssignData2(models.Model):
	created_date=models.DateField(auto_now=True)
	business_id=models.CharField(max_length=50, default='B001')
	assign_id=models.CharField(max_length=50)
	bill_id=models.CharField(max_length=50)
	filled_cylinder_deducted=models.CharField(max_length=50, default='100')
	cost_price=models.CharField(max_length=50)
	class Meta:
		db_table = "CylinderAssignData2"

class CylinderDailyReportData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	report_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	entry_date=models.CharField(max_length=50)
	per_cylinder_cost=models.CharField(max_length=50)
	profit=models.CharField(max_length=50)
	total_filled_cylinder_returned=models.CharField(max_length=50)#Total filled cylinders returned by vehicles at end of the day
	total_empty_cylinder_returned=models.CharField(max_length=50)#Total empty cylinders returned by vehicles at end of the day
	total_cylinder_sold=models.CharField(max_length=50)
	total_cylinder_assigned=models.CharField(max_length=50)
	class Meta:
		db_table = "CylinderDailyReportData"

class FuelData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	business_id=models.CharField(max_length=50)
	current_petrol_quantity=models.CharField(max_length=50, default='0')
	current_diesel_quantity=models.CharField(max_length=50, default='0')
	class Meta:
		db_table = "FuelData"

class FuelDailyData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	business_id=models.CharField(max_length=50)
	entry_id=models.CharField(max_length=50, primary_key=True)
	entry_date=models.CharField(max_length=50)
	diesel_profit=models.CharField(max_length=50)
	petrol_profit=models.CharField(max_length=50)
	total_profit=models.CharField(max_length=50)
	class Meta:
		db_table = "FuelDailyData"

#Petrol Purchase Entry
class PetrolPurchaseData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_date=models.CharField(max_length=50)
	bill_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	purchased_quantity=models.CharField(max_length=50)
	price_per_liter=models.CharField(max_length=50)
	total_price=models.CharField(max_length=50)
	bill=models.FileField(upload_to='petrolbills/', default='NA')
	class Meta:
		db_table = "PetrolPurchaseData"

class PetrolPurchaseBillsData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_id=models.CharField(max_length=50, primary_key=True)
	bill=models.FileField(upload_to='petrolbills/', default='NA')
	class Meta:
		db_table = "PetrolPurchaseBillsData"

#Diesel Purchase Entry
class DieselPurchaseData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_date=models.CharField(max_length=50)
	bill_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	purchased_quantity=models.CharField(max_length=50)
	price_per_liter=models.CharField(max_length=50)
	total_price=models.CharField(max_length=50)
	bill=models.FileField(upload_to='dieselbills/', default='NA')
	class Meta:
		db_table = "DieselPurchaseData"

class DieselPurchaseBillsData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_id=models.CharField(max_length=50, primary_key=True)
	bill=models.FileField(upload_to='dieselbills/', default='NA')
	class Meta:
		db_table = "DieselPurchaseBillsData"

#Petrol Sales
class PetrolBillData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_date=models.CharField(max_length=50)
	bill_time=models.CharField(max_length=50)
	bill_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
	price_per_liter=models.CharField(max_length=50)
	total_price=models.CharField(max_length=50)
	machine_type=models.CharField(max_length=50, default='machine_1')
	class Meta:
		db_table = "PetrolBillData"

class PetrolBillPic(models.Model):
	bill_id=models.CharField(max_length=50)
	meter_pic=models.FileField(upload_to='petrolsales/', default='NA')
	class Meta:
		db_table = "PetrolBillPic"

#Diesel Sales
class DieselBillData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	bill_date=models.CharField(max_length=50)
	bill_time=models.CharField(max_length=50)
	bill_id=models.CharField(max_length=50, primary_key=True)
	business_id=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
	price_per_liter=models.CharField(max_length=50)
	total_price=models.CharField(max_length=50)
	machine_type=models.CharField(max_length=50, default='machine_1')
	class Meta:
		db_table = "DieselBillData"

class DieselBillPic(models.Model):
	bill_id=models.CharField(max_length=50)
	meter_pic=models.FileField(upload_to='dieselsales/', default='NA')
	class Meta:
		db_table = "DieselBillPic"

class MeterReadingData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	business_id=models.CharField(max_length=50)
	photo=models.FileField(upload_to='meterreadings/', default='NA')
	fuel_type=models.CharField(max_length=15)
	class Meta:
		db_table = "MeterReadingData"