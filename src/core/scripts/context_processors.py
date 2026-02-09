from src.admin.models import Message
from src.managements.models import Contacts, SeoBlock
from src.user.models import User


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
        "new_owners": new_owners,
    }


def new_owners(request):
    new_owners = len(User.objects.filter(is_staff=False, status="NEW"))
    return {
        "new_owners": new_owners,
    }


def new_messages(request):
    if request.user.is_authenticated:
        new_messages = Message.objects.filter(
            messagestatus__user=request.user,
            messagestatus__is_read=False,
            messagestatus__is_deleted=False,
        ).order_by("-created_at")
    else:
        new_messages = Message.objects.none()
    return {
        "new_messages": new_messages,
    }
