import subprocess
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class GetVersionApiView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="Get Version API endpoint",
        description="Returns a Current version of the API",
        responses={200: dict}
    )
    def get(self, request):
        return Response({"message": "This is version v0.0.5"}, status=status.HTTP_200_OK)



@csrf_exempt
def github_update_webhook(request):
    # Only allow POST
    if request.method != "POST":
        return HttpResponseForbidden("Invalid method")

    # Check secret token
    received_token = request.headers.get("X-GITHUB-TOKEN")
    expected_token = getattr(settings, "GITHUB_WEBHOOK_SECRET", None)

    if not expected_token or received_token != expected_token:
        return HttpResponseForbidden("Invalid or missing token")

    # Log payload for debugging
    print("GitHub webhook received:", request.body)

    # --- Run deploy script ---
    deploy_script = "/home1/salidevl/teatracer-api.salidevlab.ir/update_repo.sh"

    try:
        result = subprocess.run(
            [deploy_script],
            capture_output=True,
            text=True,
            check=True
        )
        print("Deploy stdout:", result.stdout)
        print("Deploy stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        # Log error output
        print("Deploy failed stdout:", e.stdout)
        print("Deploy failed stderr:", e.stderr)
        return JsonResponse(
            {"message": "deploy failed", "error": e.stderr},
            status=500
        )

    return JsonResponse({"message": "deploy executed successfully"})
