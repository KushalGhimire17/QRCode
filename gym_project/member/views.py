from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MemberForm
from django.shortcuts import render, redirect
from .models import Member
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
# Create your views here.


def homepage_view(request):
    return render(request, 'homepage.html')


# @login_required
def qr_generator_view(request):
    if request.user.is_authenticated:
        obj = Member.objects.all()
        context = {
            'obj': obj,
        }
        return render(request, 'qrCodeGenerator.html', context)
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            messages.success(request, f'Account created for {username}!')
            return redirect('join_gym')
    else:
        form = MemberForm()
    return render(request, 'member/register.html', {'form': form})


class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        member = Member.objects.get(id=o_id)
        context = {
            "member": member
        }
        return render(request, "khaltirequest.html", context)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        o_id = request.GET.get("order_id")

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        }

        member_obj = Member.objects.get(id=o_id)

        response = requests.post(url, payload, headers=headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
            member_obj.payment_completed = True
            member_obj.save()
        else:
            success = False
        data = {
            "success": success
        }
        return JsonResponse(data)


class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        member = Member.objects.get(id=o_id)
        context = {
            "member": member
        }
        return render(request, "esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        member_obj = Member.objects.get(id=order_id)
        if status == "Success":
            member_obj.payment_completed = True
            member_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)
