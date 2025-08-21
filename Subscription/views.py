import logging
import requests
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SubscriptionModel,UserSubscriptionModel,Total_revenue
from django.contrib.auth.models import User
from datetime import  timedelta,date
from django.utils import timezone
import stripe
from .serializers import SubscriptionSerializer , UserSubscriptionSerializer , Total_revenue
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decimal import Decimal





class CreateStripeSessionView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Add this line

        package_type = request.data.get("id")
        payment_for = request.data.get("payment_for")
        user = request.user

        try:
            subscription = SubscriptionModel.objects.filter(id=package_type).first()

            if not subscription or not isinstance(subscription.package_amount, int) or subscription.package_amount <= 0:
                return Response({"message": "Invalid package amount"}, status=status.HTTP_400_BAD_REQUEST)

            price_in_cents = subscription.package_amount * 100

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": price_in_cents,
                        "product_data": {
                            "name": f"{subscription.package_type} Subscription",
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
                metadata={
                    "user_id": str(user.id),
                    "package_type": package_type,
                    "payment_for": payment_for
                }
            )
            return Response({"url": checkout_session.url})

        except stripe.error.StripeError as e:
            return Response({"message": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
logger = logging.getLogger(__name__)

@csrf_exempt

def stripe_webhook(request):
     # ✅ Add this if needed

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = "*"  #Replace with your actual key

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        logger.error("Invalid webhook signature or payload")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        package_type_id = metadata.get('package_type')

        if not all([user_id, package_type_id]):
            logger.error("Missing metadata")
            return HttpResponse(status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User not found: {user_id}")
            return HttpResponse(status=400)

        try:
            subscription = SubscriptionModel.objects.get(id=package_type_id)
            logger.info(f"Processing subscription for user {user.id} with package type {subscription.package_type}")
            
            now = timezone.now().date()
            end_date = (
                now + timedelta(days=30) if subscription.package_type == "Monthly"
                else now + timedelta(days=365) if subscription.package_type == "Yearly"
                else None
            )

            UserSubscriptionModel.objects.filter(user=user).delete()
            UserSubscriptionModel.objects.create(
                user=user,
                package_type=subscription.package_type,
                is_active=True,
                package_start_date=now,
                package_end_date=end_date,
                package_amount=subscription.package_amount,
            )

            user.subs_active = True
            user.save()

            total_revenue_obj, created = Total_revenue.objects.get_or_create(id=1)
            total_revenue_obj.total_revenue = Decimal(str(total_revenue_obj.total_revenue)) + Decimal(str(subscription.package_amount))
            total_revenue_obj.save()

            print(f"✅ Subscription created for user {user.id}")

        except SubscriptionModel.DoesNotExist:
            print(f"Subscription type not found: {package_type_id}")
            return HttpResponse(status=400)

    return HttpResponse(status=200)

@api_view(["GET", "POST"])
def subscription_list_creat(request):
    if request.method == "GET":
        subs = SubscriptionModel.objects.all()
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH'])
def subscription_update(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return Response(
            {'error': 'You are not authorized to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        subscriptions = SubscriptionModel.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(
            {'message': 'Subscriptions retrieved successfully', 'data': serializer.data},
            status=status.HTTP_200_OK
        )
    
    if request.method == 'PATCH':
        id = request.GET.get('id')
        subscription = SubscriptionModel.objects.get(id=id)
        serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Subscription updated successfully', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )