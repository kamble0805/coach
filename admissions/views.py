import qrcode
from io import BytesIO
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, FeeStructure, Payment
from django.contrib.auth.decorators import login_required

@login_required
def admission_dashboard(request):
    return render(request, 'admissions/admission_dashboard.html')

# Student Registration View (NO PAYMENT)
def register_student(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        board = request.POST['board']
        class_name = request.POST['class_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']

        # Create the Student
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            board=board,
            class_name=class_name,
            phone_number=phone_number,
            email=email,
            address=address,
        )

        messages.success(request, 'Student registered successfully. Now proceed to payment.')
        return redirect('register_payment', student_id=student.id)

    return render(request, 'admissions/register_student.html')

# Register Payment for a Student (Supports partial payments)
@login_required
def register_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    fee_structure = FeeStructure.objects.filter(board=student.board, class_name=student.class_name).first()

    if not fee_structure:
        messages.error(request, 'Fee structure not found for this board and class.')
        return redirect('view_students')

    # Get total paid so far
    previous_payments = Payment.objects.filter(student=student)
    total_paid = sum(p.amount_paid for p in previous_payments)
    total_fee = fee_structure.fee_amount if fee_structure else Decimal('0.00')
    due_amount = total_fee - total_paid

    if request.method == 'POST':
        try:
            amount_paid = Decimal(request.POST['amount_paid'])
        except:
            messages.error(request, 'Invalid payment amount.')
            return redirect('register_payment', student_id=student.id)

        payment_mode = request.POST['payment_mode']
        transaction_id = request.POST.get('transaction_id', '')

        if amount_paid <= 0:
            messages.error(request, 'Amount must be greater than zero.')
        elif amount_paid > due_amount:
            messages.error(request, f'Payment exceeds due amount. Remaining due: {due_amount}')
        else:
            Payment.objects.create(
                student=student,
                fee_structure=fee_structure,
                amount_paid=amount_paid,
                payment_mode=payment_mode,
                transaction_id=transaction_id,
            )
            messages.success(request, 'Payment recorded successfully.')
            return redirect('view_students')

    return render(request, 'admissions/register_payment.html', {
        'student': student,
        'fee_structure': fee_structure,
        'due_amount': due_amount,
        'total_paid': total_paid,
    })

# View All Students and Payment Status with Search Functionality
def view_students(request):
    search_query = request.GET.get('search', '')
    students = Student.objects.filter(first_name__icontains=search_query) | Student.objects.filter(last_name__icontains=search_query)
    student_data = []

    for student in students:
        fee_structure = FeeStructure.objects.filter(board=student.board, class_name=student.class_name).first()
        payments = Payment.objects.filter(student=student)

        total_paid = sum(p.amount_paid for p in payments)
        total_fee = fee_structure.fee_amount if fee_structure else Decimal('0.00')
        due_amount = total_fee - total_paid
        payment_details = []

        for payment in payments:
            payment_info = {
                'amount_paid': payment.amount_paid,
                'payment_mode': payment.payment_mode,
                'transaction_id': payment.transaction_id,
                'payment_date': payment.payment_date,
            }
            if payment.payment_mode == 'Online':
                payment_info['qr_code'] = generate_qr_code(payment.transaction_id)
            payment_details.append(payment_info)

        student_data.append({
            'student': student,
            'total_paid': total_paid,
            'due_amount': due_amount,
            'payment_details': payment_details,
            'fully_paid': due_amount <= 0,  # Check if full payment is made
        })

    return render(request, 'admissions/view_students.html', {
        'students': student_data,
        'search_query': search_query,
    })

# Function to generate a QR code (for online payments)
def generate_qr_code(transaction_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(transaction_id)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
