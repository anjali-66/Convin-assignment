from django.db import models

# Define choices for split methods
SPLIT_METHOD_CHOICES = [
    ('equal', 'Equal Split'),
    ('exact', 'Exact Amounts'),
    ('percentage', 'Percentage'),
]

# User model to manage user details
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# Expense model to manage expenses and their split method
class Expense(models.Model):
    title = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Function to calculate expense splits based on the selected method
    def calculate_splits(self):
        participants = self.participants.all()
        if self.split_method == 'equal':
            # Equal split: Divide total_amount by the number of participants
            split_amount = self.total_amount / participants.count()
            for participant in participants:
                participant.amount = split_amount
                participant.save()

        elif self.split_method == 'exact':
            # Exact amounts: Use the specific amounts entered for each participant
            # The amounts should already be provided by the user during entry
            pass

        elif self.split_method == 'percentage':
            # Percentage split: Ensure the percentages add up to 100%
            total_percentage = sum(participant.percentage for participant in participants)
            if total_percentage != 100:
                raise ValueError("Percentages do not add up to 100%")
            for participant in participants:
                participant.amount = (self.total_amount * participant.percentage) / 100
                participant.save()

# ExpenseParticipants model to manage who participated in each expense and how much they owe
class ExpenseParticipants(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Amount each participant owes
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage owed by participant (for percentage splits)
    is_equal_split = models.BooleanField(default=False)  # For equal splits

    def __str__(self):
        return f"{self.user.name} owes {self.amount} for {self.expense.title}"

# Balance Sheet model for generating and downloading balance sheets
class BalanceSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Balance sheet for {self.user.name} - {self.balance_amount} total"

