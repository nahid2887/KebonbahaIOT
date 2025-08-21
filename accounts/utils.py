# Twilio SMS functionality - commented out due to no balance
# from twilio.rest import Client
# from django.conf import settings

def send_otp_via_sms(phone, otp):
    # Twilio code commented out - uncomment when balance is available
    # try:
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     client.messages.create(
    #         body=f"Your OTP is {otp}",
    #         from_=settings.TWILIO_PHONE_NUMBER,
    #         to=phone
    #     )
    #     return True
    # except Exception as e:
    #     print(f"Twilio Error: {e}")
    #     return False
    
    # Temporary: Return True to simulate successful SMS sending
    print(f"SMS simulation: OTP {otp} would be sent to {phone}")
    return True
