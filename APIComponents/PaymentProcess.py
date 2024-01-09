from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from rest_framework.response import Response
from camp_admin.models import *


class ProcessPayment:
    @classmethod
    def process_payment(cls, campaign_id, card_number, exp_date, amount):
        api_login_id = '3ZA3Uk2ueQ'
        transaction_key = '8mbwJ42E6T26N6yc'
        merchant_auth = apicontractsv1.merchantAuthenticationType()
        merchant_auth.name = api_login_id
        merchant_auth.transactionKey = transaction_key

        # Create a credit card object
        credit_card = apicontractsv1.creditCardType()
        credit_card.cardNumber = card_number
        credit_card.expirationDate = exp_date

        # Create a payment object
        payment = apicontractsv1.paymentType()
        payment.creditCard = credit_card

        # Create a transaction request
        transaction_request = apicontractsv1.transactionRequestType()
        transaction_request.transactionType = "authCaptureTransaction"
        transaction_request.amount = amount
        transaction_request.payment = payment

        # Create a create transaction request
        create_request = apicontractsv1.createTransactionRequest()
        create_request.merchantAuthentication = merchant_auth
        create_request.transactionRequest = transaction_request

        # Execute the request
        controller = createTransactionController(create_request)
        controller.execute()

        # Get the response
        response = controller.getresponse()

        # Check the result
        if response is not None:
            if response.messages.resultCode == "Ok":
                print("Transaction ID:", response.transactionResponse.transId)
                print("Transaction Response Code:", response.transactionResponse.responseCode)
                print("Message Code:", response.transactionResponse.messages.message[0].code)
                print("Description:", response.transactionResponse.messages.message[0].description)
                Donations.objects.create(campaign_id=campaign_id, anonymous_location="New York", amount=amount)
                return Response("Done")
            else:
                print("Transaction failed with response code:", response.messages.message[0]['code'])
                return Response("Failed")
        else:
            print("No response received")
