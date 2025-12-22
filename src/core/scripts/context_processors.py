from src.managements.models import Contacts


def contacts(request):
    contacts = Contacts.objects.first()
    return {
        "name": contacts.name,
        "location": contacts.location,
        "address": contacts.address,
        "number": contacts.phone_number,
        "email": contacts.email,
    }
