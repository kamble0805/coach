from django.db import models
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Define the options for boards
BOARD_CHOICES = (
    ('CBSE', 'CBSE'),
    ('SSC', 'SSC'),
)

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    board = models.CharField(max_length=4, choices=BOARD_CHOICES)
    class_name = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])  # Classes 1-10
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.board} - Class {self.class_name})"

class FeeStructure(models.Model):
    board = models.CharField(max_length=4, choices=BOARD_CHOICES)
    class_name = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])  # Classes 1-10
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.board} - Class {self.class_name} - {self.fee_amount}"

import uuid

class Payment(models.Model):
    # Unique payment identifier
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Other fields
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20)  # e.g., 'Cash', 'Cheque', 'Online'
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # For online payment, can store transaction ID
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)  # For storing generated QR code image

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.amount_paid} - {self.payment_date}"

    def save(self, *args, **kwargs):
        if self.payment_mode == 'Online' and not self.qr_code:
            # Generate QR code for online payment and save it to the model
            qr_data = f"Payment for {self.student.first_name} {self.student.last_name} - {self.amount_paid} - Due Amount: {self.fee_structure.fee_amount - self.amount_paid}"
            img = qrcode.make(qr_data)
            
            # Save the QR code image into the model
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_file = InMemoryUploadedFile(img_io, None, 'payment_qr.png', 'image/png', img_io.tell(), None)
            self.qr_code = img_file

        super().save(*args, **kwargs)

    def get_due_amount(self):
        """Calculates the due amount based on the fee structure and amount paid."""
        return self.fee_structure.fee_amount - self.amount_paid

