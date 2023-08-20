from rest_framework import throttling
import random

class RandomThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 3) != 1