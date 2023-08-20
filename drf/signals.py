from django.core.signals import request_finished
from django.dispatch import receiver


@receiver(request_finished)
def a_simple_signal(sender, **kwargs):
    print(f"request finished - {dir(sender)}")
    print(f"request class - {sender.request_class}")
    print(f"response - {dir(sender.get_response)}")
    print(f"resolve request - {sender.resolve_request}")