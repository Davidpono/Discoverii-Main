import requests
from django.core.mail import send_mail
from django.utils.timezone import now

class VisitorLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        path = request.path
        location = "Unknown location"

        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            data = response.json()
            if data.get("status") == "success":
                city = data.get("city", "")
                region = data.get("regionName", "")
                country = data.get("country", "")
                location = f"{city}, {region}, {country}".strip(", ")
        except Exception as e:
            location = f"Unknown (failed to fetch location: {e})"

        try:
            send_mail(
                subject="New Visitor Logged",
                message=(
                    f"Time: {now()}\n"
                    f"IP Address: {ip}\n"
                    f"Path: {path}\n"
                    f"User Agent: {user_agent}\n"
                    f"Location: {location}"
                ),
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=["visitorlog111@outlook.com"],
                fail_silently=False,  # now raises errors if something fails
            )
        except Exception as e:
            # Log errors to console for debugging
            print(f"Failed to send visitor email: {e}")

        return self.get_response(request)
