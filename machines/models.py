# Import for model creation
from django.db import models

# Importing other elements
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Automatic Teller Machine Model
class Machine(models.Model):

    address = models.CharField(
        verbose_name = "ATM Location",
        help_text = "The address associated with this ATM.",
        max_length = 150,
        blank = False
        )

    status = models.BooleanField(
        verbose_name = "Active",
        help_text = "The current status of this ATM.",
        default = True
        )

    minimum = models.DecimalField(
        verbose_name = "Minimum Balance",
        help_text = "The minimum balance allowed on this ATM.",
        max_digits = 19,
        decimal_places = 2,
        default = 0.00,
        blank = False,
        validators = [MinValueValidator(0.01), MaxValueValidator(1000000000)]
        )

    balance = models.DecimalField(
        verbose_name = "Balance",
        help_text = "The current monetary balance of this ATM.",
        max_digits = 19,
        decimal_places = 2,
        default = 0.00,
        blank = False,
        validators = [MinValueValidator(0.01), MaxValueValidator(1000000000)]
        )

    maintenance = models.DateField(
        verbose_name = "Maintenance Date",
        help_text = "The next date in which this ATM is to be maintenanced.",
        editable = True,
        blank = True
        )

    last_refill = models.DateField(
        verbose_name = "Last Refill Date",
        help_text = "The last date in which this ATM was refilled.",
        default = timezone.now,
        editable = True,
        blank = True
        )

    next_refill = models.DateField(
        verbose_name = "Next Refill Date",
        help_text = "The next date in which this ATM is to be refilled.",
        editable = True,
        blank = True
        )

    x = models.PositiveIntegerField(
        verbose_name = "X-Axis Position",
        help_text = "This ATM's x-axis position on the map.",
        default = 1,
        validators = [MaxValueValidator(1920)]
    )

    y = models.PositiveIntegerField(
        verbose_name = "Y-Axis Position",
        help_text = "This ATM's y-axis position on the map.",
        default = 1,
        validators = [MaxValueValidator(960)]
    )

    def get_absolute_url(self):
        return reverse('model-detail-view', args = [str(self.id)])

    def __str__(self):
        return f"ATM UID: {self.id}"


# Refill Model
class Refill(models.Model):

    machine = models.ForeignKey(
        Machine,
        related_name = "refill",
        verbose_name = "Machine",
        help_text = "The machine that was refilled.",
        on_delete = models.DO_NOTHING,
        blank = False
    )

    amount = models.DecimalField(
        verbose_name = "Refill Amount",
        help_text = "The amount added to this machine.",
        max_digits = 19,
        decimal_places = 2,
        blank = False
    )

    previous = models.DecimalField(
        verbose_name = "Previous Balance",
        help_text = "The previous balance of this machine.",
        max_digits = 19,
        decimal_places = 2,
        blank = False
    )

    date_time = models.DateTimeField(
        verbose_name = "Refill Date",
        help_text = "The date this machine was refilled.",
        default = timezone.now,
        blank = False
    )

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return f"Refill #{self.id}"