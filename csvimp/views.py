from django.shortcuts import (
	render,
)

from django.http import (
    HttpResponse,
)

from .forms import (
	UploadFileForm,
	CsvModelForm,
)

from .models import (
    Csv,
)

import csv

import io

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        dfile = file.read().decode('utf-8')
        io_st = io.StringIO(dfile)

        for line in csv.reader(io_st, delimiter=','):
            print(line)

        res = "done"


        return HttpResponse(res)

    else:
        form = UploadFileForm()

    return render(request, 'csvimp/upload-file.html', {'form': form})

def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    print(row)
            obj.activated = True
            obj.save()
    return render(request, 'csvimp/upload.html', {'form': form})