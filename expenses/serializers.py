from rest_framework import serializers
from .models import User, Expense, ExpenseParticipants

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipants
        fields = ['user', 'amount', 'percentage', 'is_equal_split']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'total_amount', 'created_by', 'created_at', 'participants']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            ExpenseParticipants.objects.create(expense=expense, **participant_data)
        return expense
