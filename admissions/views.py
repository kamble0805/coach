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
# Register Payment for a Student (Supports partial payments)
@login_required
def register_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    fee_structure = FeeStructure.objects.filter(board=student.board, class_name=student.class_name).first()

    if not fee_structure:
        messages.error(request, 'Fee structure not found for this board and class.')
        return redirect('view_students')

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
            payment = Payment.objects.create(
                student=student,
                fee_structure=fee_structure,
                amount_paid=amount_paid,
                payment_mode=payment_mode,
                transaction_id=transaction_id,
            )
            messages.success(request, 'Payment recorded successfully.')
            return redirect('payment_receipt', payment_id=payment.id)

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
                'payment_id': payment.id,  # <-- Add this line
            }
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

from .models import FeeStructure

# View to register fee structure
def register_fee_structure(request):
    if request.method == 'POST':
        # Retrieve POST data from the form
        board = request.POST.get('board')
        class_name = request.POST.get('class_name')
        fee_amount = request.POST.get('fee_amount')

        # Create a new FeeStructure object
        try:
            fee_structure = FeeStructure(
                board=board,
                class_name=int(class_name),  # Ensure class_name is an integer
                fee_amount=fee_amount
            )
            fee_structure.save()

            # Success message
            messages.success(request, "Fee structure registered successfully!")
            return redirect('register_fee_structure')  # Redirect after successful registration

        except Exception as e:
            # Error handling
            messages.error(request, "There was an error in registering the fee structure. Please try again.")
            return render(request, 'admissions/register_fee_structure.html', {'error': True})
    
    return render(request, 'admissions/register_fee_structure.html')

# View to list all fee structures
def list_fee_structures(request):
    fee_structures = FeeStructure.objects.all()  # Get all fee structures
    return render(request, 'admissions/list_fee_structures.html', {'fee_structures': fee_structures})

def update_fee_structure(request, pk):
    # Fetch the FeeStructure object or return 404 if not found
    fee_structure = get_object_or_404(FeeStructure, pk=pk)
    
    # Handle the POST request to update the fee structure
    if request.method == 'POST':
        # Get the form data from the POST request
        fee_structure.board = request.POST.get('board')
        fee_structure.class_name = request.POST.get('class_name')
        fee_structure.fee_amount = request.POST.get('fee_amount')
        
        # Save the updated fee structure
        fee_structure.save()

        # Display success message
        messages.success(request, "Fee structure updated successfully!")

        # Redirect to the list of fee structures after updating
        return redirect('list_fee_structures')

    # If the request is GET, render the form with the current fee structure data
    return render(request, 'admissions/update_fee_structure.html', {
        'fee_structure': fee_structure,
        'class_range': range(1, 11)  # Passing the range of classes (1 to 10) to the template
    })

# View to delete a fee structure
def delete_fee_structure(request, pk):
    fee_structure = get_object_or_404(FeeStructure, pk=pk)

    if request.method == 'POST':
        fee_structure.delete()
        messages.success(request, "Fee structure deleted successfully!")
        return redirect('list_fee_structures')  # Redirect to the list view

    return render(request, 'admissions/delete_fee_structure.html', {'fee_structure': fee_structure})

from django.shortcuts import render
from .models import Payment
from django.http import Http404

def payment_receipt(request, payment_id):
    try:
        # Fetch the payment object based on the payment_id
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        # Handle the case where the payment doesn't exist
        raise Http404("Payment not found")

    # Pass the payment object to the template
    return render(request, 'admissions/payment_receipt.html', {'payment': payment})

