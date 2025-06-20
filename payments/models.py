from django.contrib.auth import get_user_model
from django.db import models

from materials.models import Course, Lesson

User = get_user_model()


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        TRANSFER = "transfer", "Transfer"
        STRIPE = "stripe", "Stripe"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    timestamp = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=8, choices=PaymentMethod)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_url = models.URLField(max_length=1000, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self) -> str:
        return f"{self.user} - {self.amount} usd. ({self.method})"
