from django.db import models
from datetime import date
from django.conf import settings

class UserData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	updated_record_date=models.CharField(max_length=100, null=True, blank=True)
	user_id=models.CharField(max_length=50, primary_key=True)
	store_id=models.CharField(max_length=50, null=True, blank=True)
	user_email=models.CharField(max_length=100, null=True, blank=True)
	user_mobile=models.CharField(max_length=100)
	user_name=models.CharField(max_length=100, null=True, blank=True)
	status=models.CharField(max_length=100, default='1')
	class Meta:
		db_table="UserData"

class UnitData(models.Model):
	unit_id=models.CharField(max_length=50, primary_key=True)
	unit=models.CharField(max_length=50)
	class Meta:
		db_table="UnitData"

class SubunitData(models.Model):
	subunit_id=models.CharField(max_length=50, primary_key=True)
	subunit_for=models.CharField(max_length=50)
	subunit=models.CharField(max_length=50)
	class Meta:
		db_table="SubunitData"

class StoreData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	store_id=models.CharField(max_length=50, primary_key=True)
	user_id=models.CharField(max_length=50)
	store_name=models.CharField(max_length=100, null=True, blank=True)
	store_email=models.CharField(max_length=100, null=True, blank=True)
	store_address=models.CharField(max_length=100, null=True, blank=True)
	store_gsttin=models.CharField(max_length=100, null=True, blank=True)
	store_upiid=models.CharField(max_length=100, null=True, blank=True)
	store_bank=models.CharField(max_length=100, null=True, blank=True)
	status=models.CharField(max_length=100, default='0')
	class Meta:
		db_table="StoreData"

class StoreLogoData(models.Model):
	store_id=models.CharField(max_length=50)
	store_logo=models.FileField(upload_to='storelogos/')
	class Meta:
		db_table="StoreLogoData"

class DistributerData(models.Model):
	dist_id=models.CharField(max_length=50, primary_key=True)
	store_id=models.CharField(max_length=50)
	dist_name=models.CharField(max_length=100, null=True, blank=True)
	dist_email=models.CharField(max_length=100, null=True, blank=True)
	dist_mobile=models.CharField(max_length=100)
	dist_address=models.CharField(max_length=100, null=True, blank=True)
	dist_gstin=models.CharField(max_length=100, null=True, blank=True)
	dist_balance=models.CharField(max_length=100, null=True, blank=True)
	class Meta:
		db_table="DistributerData"

class MedicineData(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	medicine_id=models.CharField(max_length=50, primary_key=True)
	store_id=models.CharField(max_length=50)
	dist_id=models.CharField(max_length=50, null=True, blank=True)
	medicine_name=models.CharField(max_length=100)
	medicine_description=models.CharField(max_length=150)
	medicine_contents=models.CharField(max_length=100)
	medicine_benifits=models.CharField(max_length=100, null=True, blank=True)
	medicine_alternatives=models.CharField(max_length=200, null=True, blank=True)
	medicine_quantity=models.CharField(max_length=10, null=True, blank=True)
	medicine_measuringunit=models.CharField(max_length=10, null=True, blank=True)
	medicine_1stripequals=models.CharField(max_length=10, null=True, blank=True)
	medicine_costprice=models.CharField(max_length=10, null=True, blank=True)
	medicine_sellprice=models.CharField(max_length=10, null=True, blank=True)
	medicine_mrp=models.CharField(max_length=10, null=True, blank=True)
	medicine_fixedrate=models.CharField(max_length=10, null=True, blank=True)
	medicine_discount=models.CharField(max_length=10, null=True, blank=True)
	medicine_gst=models.CharField(max_length=10, null=True, blank=True)
	status=models.CharField(max_length=50, default='0')
	prescription_required=models.CharField(max_length=50, default='0')
	low_stock=models.CharField(max_length=50, default='0')
	contains_expired_stock=models.CharField(max_length=50, default='0')
	class Meta:
		db_table="MedicineData"

class MedicineImageData(models.Model):
	medicine_id=models.CharField(max_length=50)
	medicine_image=models.FileField(upload_to='medicineimages/')
	class Meta:
		db_table="MedicineImageData"

class MedicineBatchData(models.Model):
	created_date=models.DateField(auto_now=True)
	delete_date=models.CharField(max_length=50, null=True, blank=True)
	batch_id=models.CharField(max_length=50, primary_key=True)
	medicine_id=models.CharField(max_length=50)
	batch_number=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
	expiry_date=models.CharField(max_length=50)
	status=models.CharField(max_length=5, default='1')
	class Meta:
		db_table="MedicineBatchData"

class BillData(models.Model):
	bill_date=models.DateField(auto_now=True)
	bill_id=models.CharField(max_length=50, primary_key=True)
	customer_id=models.CharField(max_length=50, null=True, blank=True)
	store_id=models.CharField(max_length=50)
	total_amount=models.CharField(max_length=50, null=True, blank=True)
	total_tax_amount=models.CharField(max_length=50, null=True, blank=True)
	total_discount_amount=models.CharField(max_length=50, null=True, blank=True)
	total_amount_to_pay=models.CharField(max_length=50, null=True, blank=True)
	pay_mode=models.CharField(max_length=50, null=True, blank=True)
	transaction_id=models.CharField(max_length=100, null=True, blank=True)
	bill_pdf_url=models.CharField(max_length=100, null=True, blank=True)
	delete=models.CharField(max_length=50, default='0')
	class Meta:
		db_table="BillData"

class BillItemData(models.Model):
	bill_id=models.CharField(max_length=50)
	medicine_id=models.CharField(max_length=50)
	store_id=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50, null=True, blank=True)
	amount=models.CharField(max_length=50, null=True, blank=True)
	tax_amount=models.CharField(max_length=50, null=True, blank=True)
	discount_amount=models.CharField(max_length=50, null=True, blank=True)
	amount_to_pay=models.CharField(max_length=50, null=True, blank=True)
	class Meta:
		db_table="BillItemData"

class StoreCustomerData(models.Model):
	customer_id=models.CharField(max_length=50, primary_key=True)
	store_id=models.CharField(max_length=50)
	customer_name=models.CharField(max_length=50)
	customer_mobile=models.CharField(max_length=50)
	customer_address=models.CharField(max_length=50)
	customer_doctor=models.CharField(max_length=50)
	class Meta:
		db_table="StoreCustomerData"

class CartData(models.Model):
	cart_date=models.DateField(auto_now=True)
	cart_id=models.CharField(max_length=50, primary_key=True)
	customer_id=models.CharField(max_length=50, null=True, blank=True)
	store_id=models.CharField(max_length=50)
	total_amount=models.CharField(max_length=50, null=True, blank=True)
	total_tax_amount=models.CharField(max_length=50, null=True, blank=True)
	total_discount_amount=models.CharField(max_length=50, null=True, blank=True)
	total_amount_to_pay=models.CharField(max_length=50, null=True, blank=True)
	class Meta:
		db_table="CartData"

class CartItemData(models.Model):
	cart_id=models.CharField(max_length=50)
	medicine_id=models.CharField(max_length=50)
	store_id=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50, null=True, blank=True)
	amount=models.CharField(max_length=50, null=True, blank=True)
	tax_amount=models.CharField(max_length=50, null=True, blank=True)
	discount_amount=models.CharField(max_length=50, null=True, blank=True)
	amount_to_pay=models.CharField(max_length=50, null=True, blank=True)
	class Meta:
		db_table="CartItemData"

class MedicineMasterData(models.Model):
	medicine_master_id=models.CharField(max_length=50, primary_key=True)
	medicine_master_name=models.CharField(max_length=100, null=True, blank=True)
	medicine_master_description=models.CharField(max_length=150, null=True, blank=True)
	medicine_master_contents=models.CharField(max_length=100, null=True, blank=True)
	medicine_master_benifits=models.CharField(max_length=100, null=True, blank=True)
	medicine_master_alternatives=models.CharField(max_length=200, null=True, blank=True)
	class Meta:
		db_table="MedicineMasterData"