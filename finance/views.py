import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings

from finance.models import Transaction

def file_upload(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        uploaded_files = request.FILES.getlist('files')
        results = []

        for file in uploaded_files:
            # Define your processing logic here (similar to the code you provided)
            header_row = 17
            end_row = 15

            # Use a temporary file to save the uploaded data
            with open(os.path.join(settings.MEDIA_ROOT, 'temp.csv'), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'temp.csv'), header=header_row, nrows=end_row + 1)
            print(df)
            branch_counts = {}
            if 'Branch Name' in df.columns:
                branch_counts = {}
                for _, row in df.iterrows():
                    branch_name = row['Branch Name']
                    if branch_name not in branch_counts:
                        branch_counts[branch_name] = 0
                    branch_counts[branch_name] += 1

                most_transactions_branch = max(branch_counts, key=branch_counts.get)
                transaction_count = branch_counts[most_transactions_branch]
            else:
                most_transactions_branch = "N/A"  # No 'Branch Name' column
                transaction_count = 0
            duplicate_particulars = df[df['Transaction Particulars'].duplicated(keep=False)]['Transaction Particulars'].unique()

            # Clean up the temporary file
            os.remove(os.path.join(settings.MEDIA_ROOT, 'temp.csv'))
            results.append({
                'most_transactions_branch': most_transactions_branch,
                'transaction_count': transaction_count,
                'duplicate_particulars': duplicate_particulars,
                'filename': file.name
            })
            transaction = Transaction.objects.create(
                branch_name=branch_name,
                transaction_particulars=duplicate_particulars,
                file_name=file.name
            )
            transaction.save()

        return render(request, 'result.html', {'results': results})

    return render(request, 'upload.html')
