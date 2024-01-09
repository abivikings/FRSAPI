from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from django.conf import settings
from hashlib import sha256
from .models import *
from APIComponents.PaymentProcess import ProcessPayment as prosPay


@api_view(['POST'])
def Donation(request):
    if request.method == 'POST':
        campaign_id = request.data['campaign_id']
        card_number = request.data['card_number']
        exp_date = request.data['exp_date']
        amount = request.data['amount']
        result = prosPay.process_payment(campaign_id, card_number, exp_date, amount)
        if result:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def generate_aes_key(secret_key):
    # Use hashlib to create a fixed-length key based on the SECRET_KEY
    hashed_key = sha256(secret_key.encode()).digest()
    return hashed_key[:16]  # Use the first 16 bytes for a 128-bit AES key


def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')


def decrypt_data(encrypted_data, key):
    encrypted_data = b64decode(encrypted_data.encode('utf-8'))
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode('utf-8')


@api_view(['POST'])
def SaveCardInfo(request):
    encryption_key = generate_aes_key(settings.SECRET_KEY)
    if request.method == 'POST':
        donor_id = request.data['donor_id']
        card_number = encrypt_data(request.data['card_number'], encryption_key)
        exp_date = encrypt_data(request.data['exp_date'], encryption_key)
        is_submitted = CardInfo.objects.create(donor_id=donor_id, card_number=card_number, card_exp_date=exp_date)
        if is_submitted:
            return Response('Stored')
        else:
            return Response('Failed')


@api_view(['POST'])
def DonateByStoredInfo(request):
    encryption_key = generate_aes_key(settings.SECRET_KEY)
    if request.method == 'POST':
        campaign_id = request.data['campaign_id']
        donor_id = request.data['donor_id']
        amount = request.data['amount']
        donor_card_info = list(CardInfo.objects.filter(donor_id=donor_id).values())
        card_number = decrypt_data(donor_card_info[0]['card_number'], encryption_key)
        exp_date = decrypt_data(donor_card_info[0]['card_exp_date'], encryption_key)
        result = prosPay.process_payment(campaign_id, card_number, exp_date, amount)
        if result:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

