from django.shortcuts import (
	render,
	redirect,
)

from django.views.generic import (
    ListView,
    UpdateView,
)

from django.urls import reverse_lazy


from .forms import (
	UploadFileForm,
)

from .models import (
    Imported_Payee,
    Staged_Transaction,
)

from fin.models import (
    Payee,
    Account,
)

import csv
import io

def wl(str):
    file = open("/home/mslevy35/fin23/csv_importer/log.txt", "a")
    file.write(str+"\n")
    file.close()

def chgDate(dstr):
    m = dstr[0:2]
    d = dstr[3:5]
    y = dstr[6:10]
    return (y + "-" + m + "-" + d)

def chgPncAmt(astr):
    if astr[0]=="-":
        nstr = astr[0]+astr[2:]
    else:
        nstr = astr[1:]
    return nstr

# Create your views here.
#C1
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        source = request.POST['source']
        dfile = file.read().decode('utf-8')
        io_st = io.StringIO(dfile)

        csv_reader = csv.reader(io_st, delimiter=',')

        next(csv_reader, None)

        source = str(source)

        for line in csv.reader(io_st, delimiter=','):

            #if the source is capital one
            if source == "V":
                #if the transaction is a debit (ie. an expense)
                if line[5]:
                    #if there is a payee
                    if line[3]:
                        #create new Imported_Payee object
                        imp_pay, created = Imported_Payee.objects.get_or_create(
                            imported_payee = line[3],
                        )
                        #create new Staged_Transaction object
                        stg_tran = Staged_Transaction.objects.create(
                            account = 31,
                            tdate = line[0],
                            amount = line[5],
                            imported_payee = imp_pay
                        )
                        stg_tran.save()
            elif source == "P":
                if line:
                    #Payee
                    imp_pay, created = Imported_Payee.objects.get_or_create(
                        imported_payee = line[1],
                    )
                    #create new Staged_Transaction object
                    stg_tran = Staged_Transaction.objects.create(
                        account = Account.objects.get(pk="32"),
                        tdate = chgDate(line[0]),
                        amount = chgPncAmt(line[2]),
                        imported_payee = imp_pay
                    )
                    stg_tran.save()



        return redirect('csv:imported-payees-list')

    else:
        form = UploadFileForm()

    return render(request, 'csv-importer/upload-file.html', {'form': form})

#IMPORTED PAYEE
#C2
class imported_payee_ListView(ListView):
    model = Imported_Payee
    template_name = "csv-importer/uploaded-payees-list.html"
    ordering = ['imported_payee']
#C4 [imported payee list]
class imported_payee_UpdateView(UpdateView):
	model = Imported_Payee
	template_name = "fin/update.html"
	fields = ["imported_payee", "payee"]

	def get_form(self):
	    form = super().get_form(form_class=None)
	    form.fields['payee'].queryset = Payee.objects.filter(active=True)
	    return form

	def get_success_url(self):
		next = self.request.GET.get("next")

		if next:

			return next

		return reverse_lazy('imported-payees-list')

#NEED CREATE AND DELETE VIEWS FOR IMPORTED PAYEES

#STAGED TRANSACTION
#C3
class staged_transaction_ListView(ListView):
    model = Staged_Transaction
    template_name = "csv-importer/staged-transactions-list.html"
    ordering = ['tdate']

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', None)

        if filter_val is not None:
            return Staged_Transaction.objects.filter(imported=filter_val).order_by('tdate')
        else:
            return Staged_Transaction.objects.all().order_by('tdate')

        new_context = Staged_Transaction.objects.filter(imported=filter_val).order_by('tdate')
        return new_context

    def get_context_data(self, **kwargs):
        context = super(staged_transaction_ListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', None)
        return context

