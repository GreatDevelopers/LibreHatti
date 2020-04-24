# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from librehatti.catalog.forms import ChangeRequestForm
from librehatti.catalog.models import (
    Bill,
    ChangeRequest,
    RequestStatus,
    RequestSurchargeChange,
    TaxesApplied,
)
from librehatti.config import ADMIN_GROUP, RECEIVER_EMAIL, SENDER_EMAIL
from librehatti.voucher.models import FinancialSession, VoucherId


@login_required
def request_save(request):
    """
    This function saves the new proposed values from the change request form
    in the database
    """
    if request.method == "POST":
        first_name = request.user.first_name
        last_name = request.user.last_name
        full_name = first_name + " " + last_name
        purchase_order_of_session = request.GET["order_id"]
        session_id = request.GET["session"]
        voucherid = VoucherId.objects.values("purchase_order_id").filter(
            purchase_order_of_session=purchase_order_of_session,
            session_id=session_id,
        )
        for value in voucherid:
            purchase_order = value["purchase_order_id"]
        surcharge_list = request.POST.getlist("surcharge")
        previous_value_list = request.POST.getlist("previous_value")
        new_value_list = request.POST.getlist("new_value")
        description = request.POST.get("description")
        session = FinancialSession.objects.get(pk=session_id)
        bill = Bill.objects.values("grand_total").get(
            purchase_order_id=purchase_order
        )
        taxesapplied = TaxesApplied.objects.filter(
            purchase_order=purchase_order
        )
        previous_total = bill["grand_total"]
        new_total = previous_total
        temp = 0
        for value in taxesapplied:
            if new_value_list[temp]:
                new_total = (
                    int(new_total)
                    - int(previous_value_list[temp])
                    + int(new_value_list[temp])
                )
            else:
                pass
            temp = temp + 1
        try:
            ChangeRequest.objects.get(
                purchase_order_of_session=purchase_order_of_session,
                session=session_id,
            )
            ChangeRequest.objects.filter(
                purchase_order_of_session=purchase_order_of_session,
                session=session_id,
            ).update(
                purchase_order_of_session=purchase_order_of_session,
                session=session,
                previous_total=previous_total,
                new_total=new_total,
                description=description,
                initiator=full_name,
            )
        except BaseException:
            obj = ChangeRequest(
                purchase_order_of_session=purchase_order_of_session,
                session=session,
                previous_total=previous_total,
                new_total=new_total,
                description=description,
                initiator=full_name,
            )
            obj.save()
        change_request = ChangeRequest.objects.get(
            purchase_order_of_session=purchase_order_of_session,
            session=session_id,
        )
        temp = 0
        for value in taxesapplied:
            surcharge = TaxesApplied.objects.get(
                purchase_order=purchase_order,
                surcharge__tax_name=surcharge_list[temp],
            )
            if new_value_list[temp]:

                if RequestSurchargeChange.objects.filter(
                    change_request=change_request
                ):

                    try:
                        RequestSurchargeChange.objects.get(
                            change_request=change_request, surcharge=surcharge
                        )
                        RequestSurchargeChange.objects.filter(
                            change_request=change_request, surcharge=surcharge
                        ).update(
                            change_request=change_request,
                            surcharge=surcharge,
                            previous_value=previous_value_list[temp],
                            new_value=new_value_list[temp],
                        )
                    except BaseException:
                        obj = RequestSurchargeChange(
                            change_request=change_request,
                            surcharge=surcharge,
                            previous_value=previous_value_list[temp],
                            new_value=new_value_list[temp],
                        )
                        obj.save()
                else:
                    obj = RequestSurchargeChange(
                        change_request=change_request,
                        surcharge=surcharge,
                        previous_value=previous_value_list[temp],
                        new_value=new_value_list[temp],
                    )
                    obj.save()
            else:
                try:
                    RequestSurchargeChange.objects.get(
                        change_request=change_request, surcharge=surcharge
                    )
                    RequestSurchargeChange.objects.filter(
                        change_request=change_request, surcharge=surcharge
                    ).delete()
                except BaseException:
                    pass
            temp = temp + 1
        try:
            RequestStatus.objects.get(change_request=change_request)
            RequestStatus.objects.filter(change_request=change_request).update(
                change_request=change_request,
                confirmed=0,
                cancelled=0,
                request_response=None,
            )
        except BaseException:
            obj = RequestStatus(change_request=change_request)
            obj.save()
        request_status = request_notify()
        return render(
            request, "catalog/request_success.html", {"request": request_status}
        )
    else:
        form = ChangeRequestForm()
        request_status = request_notify()
        return render(
            request,
            "catalog/change_request.html",
            {"form": form, "request": request_status},
        )


def request_notify():
    """
    This function notifies the admin that a request is pending
    for being processed
    """
    notify = RequestStatus.objects.filter(confirmed=False).filter(
        cancelled=False
    )
    if notify:
        number_request = 1
    else:
        number_request = 0

    return number_request


@login_required
@user_passes_test(
    lambda u: u.groups.filter(name=ADMIN_GROUP).count() == 1 or u.is_superuser,
    login_url="/catalog/permission_denied/",
)
def list_request(request):
    """
    This function lists the pending change requests
    """
    request_list = ChangeRequest.objects.values("id", "description")
    final_request_list = []
    for value in request_list:
        if (
            RequestStatus.objects.filter(change_request=value["id"])
            .filter(confirmed=False)
            .filter(cancelled=False)
        ):
            request_status = "Waiting"
        elif RequestStatus.objects.filter(change_request=value["id"]).filter(
            confirmed=True
        ):
            request_status = "Confirmed"
        elif RequestStatus.objects.filter(change_request=value["id"]).filter(
            cancelled=True
        ):
            request_status = "Cancelled"
        value["request_status"] = request_status
        final_request_list.append(value)
    return render(
        request, "catalog/list_request.html", {"list": final_request_list}
    )


@login_required
@user_passes_test(
    lambda u: u.groups.filter(name=ADMIN_GROUP).count() == 1 or u.is_superuser,
    login_url="/catalog/permission_denied/",
)
def view_request(request):
    """
    This function displays the information of a selected change request
    """
    request_id = request.GET["id"]
    previous_total = ChangeRequest.objects.values("previous_total").filter(
        id=request_id
    )[0]
    new_total = ChangeRequest.objects.values("new_total").filter(id=request_id)[
        0
    ]
    description = ChangeRequest.objects.values("description").filter(
        id=request_id
    )[0]
    initiator = ChangeRequest.objects.values("initiator").filter(id=request_id)[
        0
    ]
    initiation_date = ChangeRequest.objects.values("initiation_date").filter(
        id=request_id
    )[0]
    surcharge_diff = RequestSurchargeChange.objects.values(
        "surcharge__surcharge__tax_name", "previous_value", "new_value"
    ).filter(change_request=request_id)
    if (
        RequestStatus.objects.filter(change_request=request_id)
        .filter(confirmed=False)
        .filter(cancelled=False)
    ):
        request_status = "Waiting"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        confirmed=True
    ):
        request_status = "Confirmed"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        cancelled=True
    ):
        request_status = "Cancelled"
    try:
        request_response = RequestStatus.objects.values(
            "request_response"
        ).filter(change_request=request_id)[0]
    except BaseException:
        pass
    return render(
        request,
        "catalog/view_request.html",
        {
            "previous_total": previous_total,
            "new_total": new_total,
            "description": description,
            "id": request_id,
            "surcharge_diff": surcharge_diff,
            "request_status": request_status,
            "initiation_date": initiation_date,
            "initiator": initiator,
            "request_response": request_response,
        },
    )


@login_required
@user_passes_test(
    lambda u: u.groups.filter(name=ADMIN_GROUP).count() == 1 or u.is_superuser,
    login_url="/catalog/permission_denied/",
)
def accept_request(request):
    """
    This function enables the admin to accept a change request
    """
    request_id = request.GET["id"]
    today = datetime.now().date()
    user = User.objects.values("first_name", "last_name").filter(
        id=request.user.id
    )[0]
    RequestStatus.objects.filter(change_request=request_id).update(
        confirmed=True, cancelled=False, request_response=today
    )
    previous_total = ChangeRequest.objects.values("previous_total").filter(
        id=request_id
    )[0]
    new_total = ChangeRequest.objects.values("new_total").filter(id=request_id)[
        0
    ]
    description = ChangeRequest.objects.values("description").filter(
        id=request_id
    )[0]
    surcharge_diff = RequestSurchargeChange.objects.values(
        "surcharge__surcharge__tax_name", "previous_value", "new_value"
    ).filter(change_request=request_id)
    if (
        RequestStatus.objects.filter(change_request=request_id)
        .filter(confirmed=False)
        .filter(cancelled=False)
    ):
        request_status = "Waiting"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        confirmed=True
    ):
        request_status = "Confirmed"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        cancelled=True
    ):
        request_status = "Cancelled"
    change_request_obj = ChangeRequest.objects.values(
        "new_total", "purchase_order_of_session", "session_id"
    ).get(id=request_id)
    voucherid = VoucherId.objects.values("purchase_order").filter(
        purchase_order_of_session=change_request_obj[
            "purchase_order_of_session"
        ],
        session_id=change_request_obj["session_id"],
    )[0]
    Bill.objects.filter(purchase_order=voucherid["purchase_order"]).update(
        grand_total=change_request_obj["new_total"]
    )
    surchargechange = RequestSurchargeChange.objects.values(
        "surcharge_id", "new_value"
    ).filter(change_request_id=request_id)
    for value in surchargechange:
        TaxesApplied.objects.filter(id=value["surcharge_id"]).update(
            tax=value["new_value"]
        )
    plaintext = get_template("catalog/response_change_email.txt")
    content = get_template("catalog/response_change_email.html")
    temp = Context(
        {
            "previous_total": previous_total,
            "user": user,
            "new_total": new_total,
            "description": description,
            "id": request_id,
            "surcharge_diff": surcharge_diff,
            "request_status": request_status,
        }
    )
    text_content = plaintext.render(temp)
    html_content = content.render(temp)
    subject, from_email, to = "Change Request", SENDER_EMAIL, RECEIVER_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Success")


@login_required
@user_passes_test(
    lambda u: u.groups.filter(name=ADMIN_GROUP).count() == 1 or u.is_superuser,
    login_url="/catalog/permission_denied/",
)
def reject_request(request):
    """
    This function enables the admin to reject a change request
    """
    request_id = request.GET["id"]
    today = datetime.now().date()
    user = User.objects.values("first_name", "last_name").filter(
        id=request.user.id
    )[0]
    RequestStatus.objects.filter(change_request=request_id).update(
        cancelled=True, confirmed=False, request_response=today
    )
    previous_total = ChangeRequest.objects.values("previous_total").filter(
        id=request_id
    )[0]
    new_total = ChangeRequest.objects.values("new_total").filter(id=request_id)[
        0
    ]
    description = ChangeRequest.objects.values("description").filter(
        id=request_id
    )[0]
    surcharge_diff = RequestSurchargeChange.objects.values(
        "surcharge__surcharge__tax_name", "previous_value", "new_value"
    ).filter(change_request=request_id)
    if (
        RequestStatus.objects.filter(change_request=request_id)
        .filter(confirmed=False)
        .filter(cancelled=False)
    ):
        request_status = "Waiting"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        confirmed=True
    ):
        request_status = "Confirmed"
    elif RequestStatus.objects.filter(change_request=request_id).filter(
        cancelled=True
    ):
        request_status = "Cancelled"
    change_request_obj = ChangeRequest.objects.values(
        "previous_total", "purchase_order_of_session", "session_id"
    ).get(id=request_id)
    voucherid = VoucherId.objects.values("purchase_order").filter(
        purchase_order_of_session=change_request_obj[
            "purchase_order_of_session"
        ],
        session_id=change_request_obj["session_id"],
    )[0]
    Bill.objects.filter(purchase_order=voucherid["purchase_order"]).update(
        grand_total=change_request_obj["previous_total"]
    )
    surchargechange = RequestSurchargeChange.objects.values(
        "surcharge_id", "previous_value"
    ).filter(change_request_id=request_id)
    for value in surchargechange:
        TaxesApplied.objects.filter(id=value["surcharge_id"]).update(
            tax=value["previous_value"]
        )
    plaintext = get_template("catalog/response_change_email.txt")
    content = get_template("catalog/response_change_email.html")
    temp = Context(
        {
            "previous_total": previous_total,
            "user": user,
            "new_total": new_total,
            "description": description,
            "id": request_id,
            "surcharge_diff": surcharge_diff,
            "request_status": request_status,
        }
    )
    text_content = plaintext.render(temp)
    html_content = content.render(temp)
    subject, from_email, to = "Change Request", SENDER_EMAIL, RECEIVER_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Success")


@login_required
def permission_denied(request):
    """
    This function displays error when a user other than admin tries to access
    a thing not permitted to him
    """
    error_type = "Permission Denied"
    error = "You are not authorised to access it"
    temp = {"type": error_type, "message": error}
    return render(request, "error_page.html", temp)
