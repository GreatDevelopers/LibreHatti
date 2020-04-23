# from django.urls import patterns, include, url
from django.urls import re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .catalog import views as catalog_views
from .reports import views as reports_views
from .prints import views as prints_views
from .programmeletter import views as programmeletter_views
from .reports.register_generator import GenerateRegister
from .reports import register
from .reports import previous_history
from .reports.search import SearchResult
from ajax_select import urls as ajax_select_urls

admin.autodiscover()
urlpatterns = [
    re_path(r"^$", catalog_views.index, name="home"),
    re_path(
        r"^catalog/",
        include(("librehatti.catalog.urls", "catalog"), namespace="catalog"),
    ),
    re_path(
        r"^useraccounts/",
        include(("useraccounts.urls", "useraccounts"), namespace="useraccounts"),
    ),
    re_path(
        r"^print/", include(("librehatti.prints.urls", "print"), namespace="print")
    ),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^search/", reports_views.search_form, name="search_form"),
    re_path(r"^search_result/", SearchResult.as_view(), name="search_result"),
    re_path(r"^save_fields", reports_views.save_fields, name="save_fields"),
    re_path(
        r"^list_saved_registers",
        reports_views.list_saved_registers,
        name="list_saved_registers",
    ),
    re_path(r"daily_result", register.daily_report_result, name="daily_report_result"),
    re_path(
        r"consultancy_funds_report",
        register.consultancy_funds_report,
        name="consultancy_funds_report",
    ),
    re_path(r"tds_report", register.tds_report_result, name="tds_report_result"),
    re_path(r"payment_report", register.payment_register, name="payment_register"),
    re_path(
        r"suspense_clearance_register",
        register.suspense_clearance_register,
        name="suspense_clearance_register",
    ),
    re_path(r"servicetax", register.servicetax_register, name="servicetax_register"),
    re_path(r"^main_register", register.main_register, name="main_register"),
    re_path(
        r"^proforma_register", register.proforma_register, name="proforma_register"
    ),
    re_path(
        r"^non_payment_register",
        register.non_payment_register,
        name="non_payment_register",
    ),
    re_path(r"^client_register", register.client_register, name="client_register"),
    re_path(r"^material_report", register.material_report, name="material_report"),
    re_path(r"^lab_report", register.lab_report, name="lab_report"),
    re_path(
        r"^suspense_register", register.suspense_register, name="suspense_register"
    ),
    re_path(r"^registered_users", register.registered_users, name="registered_users"),
    re_path(
        r"^filter_sub_category/",
        reports_views.filter_sub_category,
        name="filter_sub_category",
    ),
    re_path(r"^bill/", prints_views.bill, name="bill"),
    re_path(r"^suspense_bill/", prints_views.suspense_bill, name="suspense_bill"),
    re_path(r"^quoted_bill/", prints_views.quoted_bill, name="quoted_bill"),
    re_path(r"^bills/", include(("librehatti.bills.urls", "bills"), namespace="bills")),
    re_path(
        r"^suspense/",
        include(("librehatti.suspense.urls", "suspense"), namespace="suspense"),
    ),
    re_path(r"^generate_register/", GenerateRegister.as_view(), name="view_register"),
    re_path(r"^history/", previous_history.history, name="history"),
    re_path(r"^details/", previous_history.details, name="details"),
    re_path(
        r"^proforma_details/",
        previous_history.proforma_details,
        name="proforma_details",
    ),
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    re_path(r"^admin/lookups/", include(ajax_select_urls)),
    re_path(
        r"^voucher/",
        include(("librehatti.voucher.urls", "voucher"), namespace="voucher"),
    ),
    re_path(r"^tinymce/", include(("tinymce.urls", "tinymce"), namespace="tinymce")),
    re_path(
        r"^programmeletter/",
        programmeletter_views.programmeletter,
        name="programmeletter",
    ),
    # re_path(r'pending_clearance_register', register.pending_clearance_register, name='pending_clearance_register'),
    # re_path(r'tada_register', register.tada_register, name='tada_register'),
    # re_path(r'tada_othercharges_register', register.tada_othercharges_register, name='tada_othercharges_register'),
    # re_path(r'client_details_according_to_amount', register.client_details_according_to_amount, name='client_details_according_to_amount')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
