from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedModel

User = get_user_model()


class BankAccount(TimeStampedModel):
    class AccountType(models.TextChoices):
        CURRENT = ("current", _("Current"))
        SAVINGS = ("savings", _("Savings"))

    class AccountStatus(models.TextChoices):
        ACTIVE = ("active", _("Active"))
        INACTIVE = ("inactive", _("Inactive"))

    class AccountCurrency(models.TextChoices):
        DOLLAR = ("us_dollar", _("US Dollar"))
        POUNT_STERLING = ("pound_sterling", _("Pound Sterling"))
        GHANA_CEDIS = ("ghana_cedis", _("Ghana Cedis"))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bank_accounts"
    )
    account_number = models.CharField(
        _("Account Number"),
        max_length=20, unique=True
    )
    account_balance = models.DecimalField(
        _("Account Balance"),
        max_digits=10,
        decimal_places=2, default=0.00
    )
    currency = models.CharField(
        _("Currency"),
        max_length=20,
        choices=AccountCurrency.choices
    )
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.INACTIVE
    )
    account_type = models.CharField(
        _("Account Type"),
        max_length=20,
        choices=AccountType.choices
    )
    is_primary = models.BooleanField(
        _("Primary Account"),
        default=False
    )
    kyc_submitted = models.BooleanField(
        _("KYC Submitted"),
        default=False
    )
    kyc_verified = models.BooleanField(
        _("KYC Verified"),
        default=False
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verfied_accounts"
    )
    verification_date = models.DateTimeField(
        _("Verification Date"),
        null=True,
        blank=True
    )
    verification_notes = models.TextField(
        _("Vefification Notes"),
        blank=True
    )
    fully_activated = models.BooleanField(
        _("Fully Activated"),
        default=False
    )


    def __str__(self) -> str:
        return f"{self.user.full_name}'s {self.get_currency_display()} - {self.get_account_type_display()} Account - {self.account_number}"

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")
        unique_together = ["user", "currency", "account_type"]

    def clean(self) -> None:
        if self.account_balance < 0:
            raise ValidationError(_("Account balance cannot be negative"))

    def save(self, *args, **kwargs) -> None:
        if self.is_primary:
            BankAccount.objects.filter(user=self.user).update(is_primary=False)
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PENDING = ("pending", _("Pending"))
        COMPLETED = ("completed", _("Completed"))
        FAILED = ("failed", _("Failed"))

    class TransactionType(models.TextChoices):
        DEPOSIT = ("deposit", _("Deposit"))
        WITHDRWAL = ("withdrawal", _("Withdrawal"))
        TRANSAFER = ("transfer", _("Transfer"))

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    amount = models.DecimalField(
        _("Amount"),
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    description = models.CharField(
        _("Description"),
        max_length=500,
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_transactions"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_transactions"
    )
    receiver_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_transactions"
    )
    sender_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_transactions"
    )
    status = models.CharField(
        _("Status"),
        choices=TransactionStatus.choices,
        max_length=20,
        default=TransactionStatus.PENDING
    )
    transacation_type = models.CharField(
        _("Transaction Type"),
        max_length=20,
        choices=TransactionType.choices
    )

    def __str__(self) -> str:
        return f"{self.transacation_type} - {self.amount} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]


