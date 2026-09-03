from django.http import JsonResponse
from taxpayers.models import Taxpayer
from .models import BrelaRecord, LandRecord

# ==================== BRELA LOOKUP ====================
def brela_lookup(request, nida_number):
    try:
        taxpayer = Taxpayer.objects.get(nida_number=nida_number)
        brela = BrelaRecord.objects.get(taxpayer=taxpayer)
        
        return JsonResponse({
            "success": True,
            "nida_number": taxpayer.nida_number,
            "full_name": taxpayer.full_name,
            "brela_number": brela.brela_number,
            "business_name": brela.business_name,
            "business_type": brela.business_type,
            "assets_value": str(brela.assets_value),
            "number_of_assets": brela.number_of_assets,
            "message": "BRELA Data Retrieved Successfully"
        })
    except Taxpayer.DoesNotExist:
        return JsonResponse({"success": False, "error": "Taxpayer not found"}, status=404)
    except BrelaRecord.DoesNotExist:
        return JsonResponse({"success": False, "error": "No BRELA record found for this NIDA"})


# ==================== LAND REGISTRY LOOKUP ====================
def land_lookup(request, nida_number):
    try:
        taxpayer = Taxpayer.objects.get(nida_number=nida_number)
        lands = taxpayer.land_records.all()
        
        land_data = [{
            "parcel_number": land.parcel_number,
            "location": land.location,
            "size_acres": str(land.size_acres),
            "estimated_value": str(land.estimated_value),
            "ownership_type": land.ownership_type,
        } for land in lands]

        total_value = sum(land.estimated_value for land in lands)

        return JsonResponse({
            "success": True,
            "nida_number": nida_number,
            "total_properties": len(lands),
            "total_estimated_value": str(total_value),
            "properties": land_data
        })
    except Taxpayer.DoesNotExist:
        return JsonResponse({"success": False, "error": "Taxpayer not found"}, status=404)


# ==================== FULL 360° VIEW ====================
def full_360_view(request, nida_number):
    try:
        # Try to lookup by TIN first, then NIDA
        try:
            taxpayer = Taxpayer.objects.get(tin_number=nida_number)
        except Taxpayer.DoesNotExist:
            taxpayer = Taxpayer.objects.get(nida_number=nida_number)

        # Use dedicated integration records when available, with the admin-entered
        # taxpayer fields as the fallback source of truth.
        brela_data = None
        try:
            brela = BrelaRecord.objects.get(taxpayer=taxpayer)
            brela_data = {
                "brela_number": brela.brela_number,
                "business_name": brela.business_name,
                "assets_value": str(brela.assets_value)
            }
        except BrelaRecord.DoesNotExist:
            if taxpayer.brela_number or taxpayer.business_name:
                brela_data = {
                    "brela_number": taxpayer.brela_number or "Not provided",
                    "business_name": taxpayer.business_name or "Not provided",
                    "assets_value": "0",
                }

        land_data = None
        try:
            lands = taxpayer.land_records.all()
            if lands.exists():
                land_data = {
                    "total_properties": lands.count(),
                    "total_value": str(sum(land.estimated_value for land in lands))
                }
        except Exception:
            land_data = None

        if land_data is None and taxpayer.land_parcel:
            land_data = {
                "total_properties": 1,
                "total_value": "0",
                "properties": [{
                    "parcel_number": taxpayer.land_parcel,
                    "location": "Admin record",
                    "size_acres": "0",
                    "estimated_value": "0",
                    "ownership_type": "Admin record",
                }],
            }

        return JsonResponse({
            "success": True,
            "taxpayer": {
                "tin_number": taxpayer.tin_number or taxpayer.nida_number,
                "nida": taxpayer.nida_number,
                "name": taxpayer.full_name,
                "phone": taxpayer.phone_number,
                "email": taxpayer.email or "",
                "business_name": taxpayer.business_name or "",
                "brela_number": taxpayer.brela_number or "",
                "land_parcel": taxpayer.land_parcel or "",
                "estimated_income": str(taxpayer.estimated_income),
                "tax_compliance_score": taxpayer.tax_compliance_score,
                "credit_score": taxpayer.credit_score,
            },
            "brela": brela_data,
            "land": land_data,
            "overall_risk": "High" if taxpayer.estimated_income > 20000000 else "Medium",
            "recommendation": "Recommend detailed audit" if taxpayer.tax_compliance_score < 60 else "Low risk taxpayer"
        })
    except Taxpayer.DoesNotExist:
        return JsonResponse({"success": False, "error": "Taxpayer not found"}, status=404)