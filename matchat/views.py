import os
import urllib

from decouple import config

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from chatbot.dialogflowApi import update_intent, batch_update_intents
from chatbot.dialogflow_ID import intent_id
from .models import Product, Photo
from .forms import ProductForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import randint


from django.http import HttpResponse, JsonResponse
from django.views import templates
import requests
import json


def main(request):
    product_list = Product.objects.order_by('-create_date')
    context = {'product_list': product_list}
    return render(request, 'main.html', context)


def index(request):
    # 상품 목록
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'low':
        product_list = Product.objects.order_by('price')
    elif so == 'high':
        product_list = Product.objects.order_by('-price')
    elif so == 'old':
        product_list = Product.objects.order_by('create_date')
    else:
        product_list = Product.objects.order_by('-create_date')

    # 검색
    if kw:
        product_list = product_list.filter(
            Q(name__icontains=kw) |  # 상품명 검색
            Q(content__icontains=kw) |  # 설명 검색
            Q(author__username__icontains=kw)  # 판매자 검색
        ).distinct()
    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)

    context = {'product_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'matchat/product_list.html', context)


def detail(request, product_id):
    # 상세 페이지
    product = get_object_or_404(Product, pk=product_id)
    response = [
        "상품 이름은 " + product.name + "입니다.",
        "상품 가격은 " + product.price + "원 입니다.",
        "수령할 위치는 " + product.place + "입니다.",
        "상세 설명:" + product.content,
        product.kiosk_photo,
        "사용 기간은 " + product.use_period + "입니다.",
        product.name,
        "판매자 이름은 " + str(product.author) + "입니다."
    ]

    name = list(intent_id.keys())
    # update_intent(name[0], response[0], 0)
    # for i in range(len(response)):
    #     if i == 4:
    #         update_intent(name[i], response[i], 1)
    #     else:
    #         update_intent(name[i], response[i], 0)

    batch_update_intents(list(intent_id.keys()), response)

    context = {'product': product}
    return render(request, 'matchat/product_detail.html', context)


def my_detail(request, product_id):
    # 상세 페이지
    # product = get_object_or_404(Product, pk=product_id)
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'matchat/my_product_detail.html', context)


def detect_photo(img, product):
    img_str = str(img)
    img_url = "http://ec2-3-39-94-66.ap-northeast-2.compute.amazonaws.com/media/" + str(product.author) + "/" + str(product.name) + "/" + img_str
    data = {"url": img_url}
    res = requests.post("http://ec2-3-39-94-66.ap-northeast-2.compute.amazonaws.com/predict", data=data).json()
    return res


@login_required(login_url='account:login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.create_date = timezone.now()
            product.author = request.user
            product.key = randint(10000, 99999)
            product.save()
            for img in request.FILES.getlist('photo'):
                photos = Photo()
                photos.product = product
                photos.photo = img
                photos.save()
                product.web_result = detect_photo(img, product)
                product.save()
            return redirect('matchat:main')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'matchat/product_form.html', context)


@login_required(login_url='account:login')
def product_modify(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('matchat:detail', product_id=product.id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            product.photo_set.all().delete()
            for img in request.FILES.getlist('photo'):
                photos = Photo()
                photos.product = product
                photos.photo = img
                photos.save()
            return redirect('matchat:detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'matchat/product_form.html', context)


@login_required(login_url='account:login')
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('account:detail', product_id=product.id)
    product.delete()
    return redirect('matchat:main')


@login_required(login_url='account:login')
def product_reserve(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.reservation = request.user
    product.state = '2'  # 결제를 하면 상태 2(결제완료) 로 변경
    product.save()
    return redirect('matchat:detail', product_id=product.id)


# 예약 취소를 위한 함수 -> 예약 기능이 사라져서 사용 X
@login_required(login_url='account:login')
def product_reserve_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.reservation = None
    product.state = '1'  # 취소를 하면 1(등록완료) 로 변경
    product.save()
    return redirect('matchat:detail', product_id=product.id)


def product_my(request):
    product_list = Product.objects.order_by('-create_date')
    context = {'product_list': product_list}
    return render(request, 'matchat/my_product_list.html', context)


@login_required(login_url='account:login')
def pay(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.state='2'
    product.reservation = request.user # reservation = 구매자, 구매자는 detail 페이지에서 인증번호 봐야하므로 reservation 업데이트
    product.save()
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + config('ADMIN_KEY'),  # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",  # 테스트용 코드
            "partner_order_id": '1',  # 주문번호
            "partner_user_id": request.user.username,  # 유저 아이디
            "item_name": product.key,  # 구매 물품 이름
            "quantity": "1",  # 구매 물품 수량
            "total_amount": product.price,  # 구매 물품 가격
            "tax_free_amount": '0',  # 구매 물품 비과세
            "approval_url": "http://ec2-3-39-94-66.ap-northeast-2.compute.amazonaws.com/matchat/pay/approval",
            "cancel_url": "http://ec2-3-39-94-66.ap-northeast-2.compute.amazonaws.com/matchat/pay/cancel",
            "fail_url": "http://ec2-3-39-94-66.ap-northeast-2.compute.amazonaws.com/matchat/pay/fail",
        }
        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']  # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']  # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)
    return render(request, 'matchat/pay.html')


def approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + config('ADMIN_KEY'),
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": '1',      # 주문번호
        "partner_user_id": request.user.username,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render(request, 'matchat/approval.html', context)


def cancel(request):
    return render(request, 'matchat/cancel.html')


def fail(request):
    return render(request, 'matchat/fail.html')
