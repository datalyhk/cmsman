from django.db import models
from cmssys.models import CMSModel, Encounter, TextBooleanField
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class Bill(CMSModel):
    """
    Maps to CMS table to track bills charged to patient:encounter_id
    """

    version = models.BigIntegerField(default=1)
    date_created = models.DateTimeField(editable=False)
    last_updated = models.DateTimeField()
    encounter = models.ForeignKey(
        Encounter, on_delete=models.PROTECT,
        db_column='encounter_id'
    )
    invoice_print_status = models.BooleanField(default=False)
    receipt_print_status = models.BooleanField(default=False)
    total = models.FloatField()
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    transaction_code = models.CharField(max_length=255, blank=True, null=True)
    unbalance_amt = models.FloatField(default=0)
    daily_sequence_per_clinic = models.IntegerField(blank=True, null=True)
    payment_update_count = models.IntegerField(blank=True, null=True)
    temp_wq_arrive_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bill'
        app_label = 'cmsacc'
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.date_created} | Encounter #{self.encounter_id} Total ${self.total}; Unbalanced ${self.unbalance_amt}"
    
    def save(self, *args, **kwargs):
        """On save, update timestamps with offset"""
        if not self.id:
            self.date_created = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS) 
        self.last_updated = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS)
        return super().save(*args, **kwargs)

class BillDetail(CMSModel):
    """
    Maps to CMS table to track billing details
    """

    version = models.BigIntegerField(default=0)
    bill = models.ForeignKey(
        'Bill', on_delete=models.PROTECT,
        db_column='bill_id'
        )
    # billed_amount = standard x discount_percent
    billed_amount = models.FloatField()
    charge_item = models.ForeignKey(
        'ChargeItem', on_delete=models.PROTECT,
        db_column='charge_item_id'
    )
    remarks = models.TextField(blank=True, null=True)

    # standard - standard cost of charge item
    standard = models.FloatField()

    # bill_details_idx - index number of item linked to the same bill_id
    bill_details_idx = models.IntegerField(blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    last_updated = models.DateTimeField()
    quantity = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bill_detail'
        app_label = 'cmsacc'
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.last_updated} | #{self.bill.id}.{self.bill_details_idx}: {self.charge_item.alias} - ${self.billed_amount} (Std ${self.standard})"

    def save(self, *args, **kwargs):
        """On save, update timestamps with offset"""
        self.last_updated = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS)
        return super().save(*args, **kwargs)

class Cashbook(CMSModel):
    """
    CMS table to track cash transactions
    """
    BILL = 'bill'  # all lowercase used in CMS app
    DELIVERY = 'Delivery'
    DISPENSARY = 'Dispensary'
    REMARK_CHOICES = [
        (DELIVERY, 'Delivery'),
        (DISPENSARY, 'Dispensary'),
    ]
    ENTRY_TYPE_CHOICES = [
        (BILL, 'Bill'),
        (DELIVERY, 'Delivery'),
    ]

    version = models.BigIntegerField(default=0)
    amount = models.FloatField()
    date_created = models.DateField(editable=False)
    last_updated = models.DateTimeField()
    editable = models.BooleanField(default=False)

    # reference_id - refers to if in CMS table specified in entry_type
    # E.g. for entry_type='bill', reference_id refers to bill_id
    reference_id = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(choices=REMARK_CHOICES, blank=True, null=True)
    entry_type = models.CharField(
        choices=ENTRY_TYPE_CHOICES,
        max_length=255, blank=True, null=True,
        db_column='type'
        )
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cashbook'
        app_label = 'cmsacc'
        verbose_name_plural = 'Cashbook'
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} | {self.date_created} {self.entry_type} #{self.reference_id} - ${self.amount}"

    def save(self, *args, **kwargs):
        """On save, update timestamps with offset"""
        if not self.id:
            self.date_created = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS) 
        self.last_updated = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS)
        return super().save(*args, **kwargs)

class ChargeItem(CMSModel):
    """
    CMS table to track service item charge
    """

    version = models.BigIntegerField(default=0)
    alias = models.CharField(max_length=255)
    # cp_prescription_amt - '1' for medication, '0' for all other items
    cp_prescription_amt = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    description_chinese = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    owner_id = models.BigIntegerField(blank=True, null=True)
    standard_amount = models.FloatField()
    cp_consumable_amt = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    sys_is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'charge_item'
        app_label = 'cmsacc'
        ordering = ['alias']

    def __str__(self):
        return f"{self.alias} | ${self.standard_amount} - {self.description_chinese} {self.description}"

class PaymentMethod(CMSModel):

    version = models.BigIntegerField()
    payment_method = models.CharField(max_length=255)
    payment_method_chinese = models.CharField(max_length=255)
    acc_receivable_fg = TextBooleanField()
    reference = models.CharField(max_length=255, blank=True, null=True)
    active = TextBooleanField()

    class Meta:
        managed = False
        db_table = 'payment_method'

class PaymentDetails(CMSModel):

    version = models.BigIntegerField()
    amount = models.FloatField()
    bill = models.ForeignKey(
        'Bill', on_delete=models.PROTECT,
        db_column='bill_id'
        )
    date_created = models.DateField(editable=False)
    last_updated = models.DateTimeField()
    payment_method = models.ForeignKey(
        'PaymentMethod', on_delete=models.PROTECT,
        db_column='payment_method_id'
        )
    remark = models.TextField(blank=True, null=True)
    status_print = models.IntegerField()
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    clear_payment = TextBooleanField()
    paid_amt = models.FloatField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)
    receive_method_id = models.BigIntegerField(blank=True, null=True)
    # receive_method_id not used (NULL)

    class Meta:
        managed = False
        db_table = 'payment_details'

    def save(self, *args, **kwargs):
        """On save, update timestamps with offset"""
        if not self.id:
            self.date_created = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS) 
        self.last_updated = timezone.now() + timedelta(hours=settings.CMS_OFFSET_HRS)
        return super().save(*args, **kwargs)