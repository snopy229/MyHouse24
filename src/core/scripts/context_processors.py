from src.managements.models import Contacts, SeoBlock


def contacts(request):
    contacts = Contacts.objects.first()
    if not contacts:
        seo_block = SeoBlock.objects.create()
        contacts = Contacts.objects.create(seo_block=seo_block)
    return {
        "name": contacts.name,
        "location": contacts.location,
        "address": contacts.address,
        "number": contacts.phone_number,
        "email": contacts.email,
    }
