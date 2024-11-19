import logging
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.urls import reverse
from django.shortcuts import render

amount_param = openapi.Parameter(
    'amount', openapi.IN_QUERY, description="Payment amount in IRR", type=openapi.TYPE_INTEGER, default=50000
)
mobile_param = openapi.Parameter(
    'user_mobile_number', openapi.IN_QUERY, description="User mobile number", type=openapi.TYPE_STRING, default="+989112221234"
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[amount_param, mobile_param],
    operation_summary="Redirect to Payment Gateway",
    operation_description="Redirects the user to the bank's payment gateway with the specified amount and mobile number.",
    responses={200: "HTML page redirecting user to bank gateway", 500: "Internal Server Error"},
    tags=["Payment Gateway"]
)
@api_view(['GET'])
@csrf_exempt
def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = 5000000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = "09332368885"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        callback_url = request.build_absolute_uri(reverse('callback_gateway'))
        bank.set_client_callback_url(callback_url)
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, "redirect_to_bank.html", context=context)
    except AZBankGatewaysException as e:
        logging.critical(e)
        return render(request, "redirect_to_bank.html")


@swagger_auto_schema(
    method='get',
    operation_summary="Payment Callback",
    operation_description="Handles the callback from the bank after the payment is processed.",
    responses={
        200: openapi.Response("Success", examples={"text": "پرداخت با موفقیت انجام شد."}),
        404: "Not Found - Invalid tracking code",
        500: "Internal Server Error - Unable to verify payment"
    },
    tags=["Payment Gateway"]
)
@api_view(['GET'])
@csrf_exempt
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )
