from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from ledger.models import (
    Expense,
)
from .models import (
    RegisteredDrug,
    Company,
)

from cmsinv.models import (
    InventoryItem
)

from inventory.models import (
    Item, DeliveryItem, ItemType
)

class RegisteredDrugList(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    """List of registered drugs"""
    permission_required = ('drugdb.view_registereddrug', )
    template_name = 'drugdb/drug_list.html'
    model = RegisteredDrug
    context_object_name = 'drug_list'
    paginate_by = 20
    last_query = ''
    last_query_count = 0
    disp_type = ''

    def get_queryset(self):
        query = self.request.GET.get('q')
        if self.request.GET.get('t'):
            self.disp_type = self.request.GET.get('t')
        if self.disp_type == '1':   # Display unlinked
            object_list = RegisteredDrug.objects.filter(item=None)
        elif self.disp_type == '2':  # Display linked
            object_list = RegisteredDrug.objects.exclude(item=None)
        elif self.disp_type == '3':  # Display inactive
            object_list = RegisteredDrug.objects.filter(is_active=True)
        else:
            object_list = RegisteredDrug.objects.all()
        if query:
            self.last_query = query
            object_list = object_list.filter(
                Q(name__icontains=query) |
                Q(reg_no__icontains=query) |
                Q(ingredients__name__icontains=query)
            )
            self.last_query_count = object_list.count
        else:
            self.last_query = ''
            self.last_query_count = object_list.count
        return object_list.distinct().order_by('name')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['last_query'] = self.last_query
        data['last_query_count'] = self.last_query_count
        data['disp_type'] = self.disp_type
        return data

class RegisteredDrugDetail(DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    """Display details for registered drug"""
    permission_required = ('drugdb.view_registereddrug', )
    model = RegisteredDrug
    template_name = 'drugdb/drug_detail.html'
    context_object_name = 'drug_detail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

class CompanyList(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    """List of Companies"""
    permission_required = ('drugdb.view_company', )
    template_name = 'drugdb/company_list.html'
    model = Company
    context_object_name = 'company_list'
    paginate_by = 20

    def get_queryset(self):
        return Company.objects.all()
  
class DrugDetailMatch(ListView, LoginRequiredMixin):
    """
    CMS Inventory Item List Matching Non-CMS Delivery Record
    """
    model = InventoryItem
    template_name = "drugdb/drug_detail_match.html"
    context_object_name = 'match_item_list_obj'
    drug_reg_no = ''
    keyword = ''
    ingredients = ''
    drug_obj = None
    deliveryitem_obj_list = None
    cmsitem_obj = None
    item_obj = None
    drug_list = None
    match_item_list_obj = None
    disp_drug_list = False

    def dispatch(self, request, *args, **kwargs):
        if 'reg_no' in kwargs:
            self.drug_reg_no = kwargs['reg_no']
            try:
                self.cmsitem_obj = InventoryItem.objects.get(registration_no=self.drug_reg_no)
            except InventoryItem.DoesNotExist:
                self.cmsitem_obj = None
            try:
                self.item_obj = Item.objects.get(reg_no=self.drug_reg_no)
            except Item.DoesNotExist:
                self.item_obj = None
            try:
                self.drug_obj = RegisteredDrug.objects.get(reg_no=self.drug_reg_no)
            except RegisteredDrug.DoesNotExist:
                self.drug_obj = None 
                print("Error: Registered Drug No. does not exist")
            try:
                self.deliveryitem_obj_list = DeliveryItem.objects.filter(item__reg_no=self.drug_reg_no)[:5]
            except DeliveryItem.DoesNotExist:
                self.deliveryitem_obj_list = None
        else:
            print("Error: missing reg_no")
        if request.GET.get('r') and request.GET.get('r') == '1':
            self.disp_drug_list = True
        else:
            self.disp_drug_list = False
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Try get first 3 ingredients from Registered Drug
        keyword = ''
        if self.drug_obj:
            if self.drug_obj.ingredients_list:
                try:
                    related_words = self.drug_obj.ingredients_list.split(',')
                except:
                    related_words = []
            else:
                # If no ingredient, try product_name
                try:
                    related_words = self.drug_obj.name.split(' ')
                except:
                    related_words = []
            if len(related_words) > 0:
                # Assign first non-numeric string to keyword for filter
                index = 0
                while keyword == '' and index < len(related_words):
                    try:
                        float(related_words[index])
                        index += 1
                    except ValueError:
                        keyword = str(related_words[index])
                        index += 1
                if self.disp_drug_list:
                    self.drug_list = RegisteredDrug.objects.filter(
                        Q(ingredients__name__icontains=keyword) |
                        Q(name__icontains=keyword)
                    ).order_by('name')[:50]
                else:
                    self.match_item_list_obj = InventoryItem.objects.filter(
                        Q(product_name__icontains=keyword) |
                        Q(ingredient__icontains=keyword)
                    ).order_by('product_name')[:50]
        else:
            self.drug_list = None
            self.match_item_list_obj = None
        data['drug_obj'] =  self.drug_obj
        data['cmsitem_obj'] = self.cmsitem_obj
        data['item_obj'] = self.item_obj
        data['deliveryitem_obj_list'] = self.deliveryitem_obj_list
        data['drug_list'] = self.drug_list
        data['match_item_list_obj'] = self.match_item_list_obj
        data['related_keyword'] = keyword
        return data

    def get_queryset(self):
        if self.drug_obj:
            self.keyword = self.drug_obj.name
            self.ingredients = self.drug_obj.ingredients_list
        else:
            print('Error: no matching reg no.')
        if self.keyword == None:
            self.keyword = ''
        if self.ingredients == None:
            self.ingredients = ''
        object_list = InventoryItem.objects.filter(
            Q(product_name__icontains=self.keyword) |
            Q(generic_name__icontains=self.keyword) |
            Q(alias__icontains=self.keyword) |
            Q(ingredient__icontains=self.ingredients)
        ).order_by('discontinue').exclude(registration_no=self.drug_reg_no)[:100]
        return object_list


@login_required
@permission_required('drugdb.change_registereddrug', )
def LinkCMSItemModalView(request, *args, **kwargs):
    if kwargs['reg_no']:
        drug_obj = get_object_or_404(RegisteredDrug, reg_no=kwargs['reg_no'])
    else:
        print("Error: no reg_no")
    if kwargs['cmsitem_id']:
        cmsitem_obj = get_object_or_404(InventoryItem, pk=kwargs['cmsitem_id'])
    else:
        print("Error: no cmsitem_id")
    uri = request.GET.get('next', reverse('drugdb:DrugDetailMatch', args=(drug_obj.reg_no,)))

    context = {
        'drug_obj': drug_obj,
        'cmsitem_obj': cmsitem_obj,
    }
    # If POST request confirm sync, add data to CMS
    if request.method == "POST":
        doUpdateCMSProductDetails = request.POST.get('updateCMSProductDetails') == '1'
        # Update CMS Product Name and Ingredients if checked
        if doUpdateCMSProductDetails:
            cmsitem_obj.product_name = drug_obj.name
            cmsitem_obj.ingredient = drug_obj.ingredients_list
            cmsitem_obj.save()

        # Create new corresponding inventory.Item if not existing
        new_item_data = {
            'name': cmsitem_obj.product_name,
            'cmsid': cmsitem_obj.id,
            'reg_no': drug_obj.reg_no,
            'item_type': ItemType.objects.get(value=1),
            'is_active': True,
            'updated_by': request.user.username,
            'last_updated': timezone.now(),
        }
        item_obj, created = Item.objects.update_or_create(
            cmsid=cmsitem_obj.id, defaults=new_item_data
        )
        if created:
            print(f"Item created: {item_obj}")
        else:
            print(f"Existing item updated: {item_obj}")

        # Update Reg Drug cms_id and item_id
        drug_obj.itemid = item_obj.id
        drug_obj.item = item_obj
        drug_obj.save()

        return redirect(uri)
    
    return render(request, "drugdb/link_cms_item_modal.html", context)