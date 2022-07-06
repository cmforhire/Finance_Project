from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

# grab the current user model
User = get_user_model()
# grab the routing number
account_routing = settings.ROUTING


def gen_account_number():
    """
    generate an account number between 8-12 digits
    """
    while True:
        check_num = str(random.randint(10000000, 999999999999))  # grab a random integer
        # confirm the value does not already exist
        if BankAccount.objects.filter(account_number=check_num).exists():
            continue
        break
    return check_num


# Define the bank account model (creates a checking/savings account with a 0 balance for the user)
class BankAccount(models.Model):
    CREDIT = (
        ('Needs Work', 'Needs Work'),
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
        ('Excellent', 'Excellent')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    checking = models.FloatField()
    savings = models.FloatField()
    credit = models.CharField(max_length=10, choices=CREDIT, default='Good')
    routing = models.CharField(default=f'{account_routing}')
    account_number = models.CharField(max_length=12, unique=True, default='')

    # ensure the checking/saving account values are rounded to two decimal places
    def save(self, *args, **kwargs):
        self.checking = round(self.checking, 2)
        self.savings = round(self.savings, 2)
        self.account_number = gen_account_number()
        super(BankAccount, self).save(*args, **kwargs)


# model that will record the transactions that occur with the account
class Transactions(models.Model):
    ACTION = (
        ('outgoing', 'outgoing'),
        ('incoming', 'incoming')
    )
    # what was the source of the payment
    CREDIT_OR_DEBIT = (
        ('credit', 'credit'),
        ('debit', 'debit')
    )
    # user associated with the account
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # was the money going out or coming in
    action = models.CharField(max_length=8, choices=ACTION, default='outgoing')
    # the amount involved in the transaction
    amount = models.FloatField()
    # company associated with the payment
    company = models.CharField(max_length=25, default='Misc.', blank=False, null=False)
    # credit card or bank account
    source = models.CharField(max_length=6, choices=CREDIT_OR_DEBIT, default='debit')


class CreditCard(models.Model):
    # the user associated with the account
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the date the user received the credit card
    approval_date = models.DateTimeField(default=timezone.now)
    # the allowed credit limit
    credit_limit = models.FloatField()
    # the amount utilized
    utilization = models.FloatField()
    # the set apr
    apr = models.FloatField()

    # ensure the credit limit and credit utilized values are rounded to two decimal places
    def save(self, *args, **kwargs):
        self.credit_limit = round(self.credit_limit, 2)
        self.utilization = round(self.utilization, 2)
        super(CreditCard, self).save(*args, **kwargs)


