from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import csv
from .models import Account
from decimal import Decimal

def import_accounts(request):
    if request.method == "POST" and request.FILES.get("file"):
        csv_file = request.FILES["file"]
        try:
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for index, row in enumerate(reader):
                if index == 0 and row[0].lower() == "id":
                    continue
                if len(row) != 3:
                    return HttpResponse(f"Invalid row format at line {index + 1}: {row}")

                # Extract data from the row
                account_id = row[0]
                name = row[1]
                balance = row[2]

                try:
                    balance = float(balance)
                except ValueError:
                    return HttpResponse(f"Invalid balance at line {index + 1}: {balance}")

                # Create or update the account in the database
                Account.objects.update_or_create(
                    id=account_id,
                    defaults={"name": name, "balance": balance},
                )

            return HttpResponse("Accounts imported successfully!")
        except Exception as e:
            return HttpResponse(f"Error processing file: {str(e)}")
    return render(request, "import.html")

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, "list.html", {"accounts": accounts})


def transfer_funds(request):
    if request.method == "POST":
        from_account_id = request.POST.get("source_id")
        to_account_id = request.POST.get("destination_id")
        amount = request.POST.get("amount")

        try:
            # Convert amount to Decimal
            amount = Decimal(amount)

            # Fetch accounts
            from_account = get_object_or_404(Account, id=from_account_id)
            to_account = get_object_or_404(Account, id=to_account_id)

            # Ensure sufficient balance in the source account
            if from_account.balance < amount:
                return HttpResponse("Insufficient balance in the source account.")

            # Perform the transfer
            from_account.balance -= amount
            to_account.balance += amount

            # Save changes
            from_account.save()
            to_account.save()

            return HttpResponse("Funds transferred successfully!")
        except Exception as e:
            return HttpResponse(f"Error during transfer: {str(e)}")
    else:
        accounts = Account.objects.all()
        return render(request, "transfer.html", {"accounts": accounts})
