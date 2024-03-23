from django.shortcuts import render

from django.urls import reverse_lazy

from .models import fcflow

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.
def index(request):
    template='proj_1/main.html'
    return render(request, template)

def get_fed_tax(ft):
    if ft<190750:
        r=-0.22
        s=9385
    elif ft<364200:
        r=-0.24
        s=13200
    elif ft<462500:
        r=-0.32
        s=42336
    elif ft<693750:
        r=-0.35
        s=56211
    else:
        r=-0.37
        s=70086
    return (ft*r)+s

def calc_ny_tax(t):
	if t<17150:
		r=-0.04
		a=0
		s=0
	elif t<23600:
		r=-0.045
		a=-686
		s=17150
	elif t< 27900:
		r=-0.0525
		a=-976
		s=23600
	elif t< 161550:
		r=-0.055
		a=-1202
		s=27900
	elif t< 323200:
		r=-0.0600
		a=-8553
		s=161550
	elif t< 2155350:
		r=-0.0685
		a=-18252
		s=323200
	elif t< 5000000:
		r=-0.0965
		a=-143754
		s=2155350
	return ((t-s)*r)+a


def get_ny_tax(i):
	sded = 16050
	dexp = 2000
	t = i-sded-dexp

	if i>107650:
		if t <= 161550:
			l3=-0.055*t

			if i>= 157650:
				tax=l3
				return tax

			else:
				l4=calc_ny_tax(t)
				l5=l3-l4
				l6=i-107650
				l7=l6/50000
				l8=l5*l7
				tax=l4+l8
				return tax

	if t<323200:
		l3=calc_ny_tax(t)
		l4=-333
		l5=-807
		l6=-i+161550
		if l6>-50000:
			l7=l6
		else:
			l7=-50000
		l8=l7/-50000
		l9=l5*l8
		tax=l3+l4+l9
	elif t<2155350:
		l3=calc_ny_tax(t)
		l4=-1140
		l5=-2747
		l6=-i+323200
		if l6>-50000:
			l7=l6
		else:
			l7=-50000
		l8=l7/-50000
		l9=l5*l8
		tax=l3+l4+l9
	else:
		tax = 0

	return tax

def get_fed_wh(ft, ewh):
    #Federal WH Calcs
    if ft < 562:
        fwh = 0

    elif ft < 1008:
        fwh = 0 + (-0.10 * (ft - 562))

    elif ft < 2375:
        fwh = -44.60 + (-0.12 * (ft - 1008))

    elif ft < 4428:
        fwh = -208.64 + (-0.22 * (ft - 2375))

    elif ft < 7944:
        fwh = -660.30 + (-0.24 * (ft - 4428))

    elif ft < 9936:
        fwh = -1504.14 + (-0.32 * (ft - 7994))

    elif ft < 23998:
        fwh = -2141.58 + (-0.35 * (ft - 9936))

    else:
        fwh = -7063.28 + (0.37 * (ft - 23998))

    fwh = round(fwh+ewh, 2)
    return fwh

def get_ny_wh(ft):
    #NY State Tax
    #assumes single / 0 allowences

    ny_ex = 284.60

    ny_nw = ft - ny_ex

    if ny_nw < 327:
        nwh = ((ny_nw - 0)     * -0.0400) - 0
    elif ny_nw < 450:
        nwh = ((ny_nw - 327)   * -0.0450) - 13.08
    elif ny_nw < 535:
        nwh = ((ny_nw - 450)   * -0.0525) - 18.62
    elif ny_nw < 3102:
        nwh = ((ny_nw - 535)   * -0.0550) - 23.08
    elif ny_nw < 3723:
        nwh = ((ny_nw - 3102)  * -0.0600) - 164.27
    elif ny_nw < 4140:
        nwh = ((ny_nw - 3723)  * -0.0714) - 201.54
    elif ny_nw < 6063:
        nwh = ((ny_nw - 4140)  * -0.0764) - 231.31
    elif ny_nw < 8285:
        nwh = ((ny_nw - 6063)  * -0.0650) - 378.15
    elif ny_nw < 10208:
        nwh = ((ny_nw - 8285)  * -0.1101) - 522.54
    elif ny_nw < 41444:
        nwh = ((ny_nw - 10208) * -0.0735) - 734.31
    else:
        nwh = 0

    nwh = round(nwh, 2)
    return nwh

def get_nj_wh(njt):
    #NJ State Tax

    nj_nw = njt

    if nj_nw < 769:
        jwh = ((nj_nw - 0)     * -0.015) - 0
    elif nj_nw < 1346:
        jwh = ((nj_nw - 769)   * -0.020) - 12
    elif nj_nw < 1538:
        jwh = ((nj_nw - 1346)   * -0.039) - 23
    elif nj_nw < 2885:
        jwh = ((nj_nw - 1538)   * -0.061) - 31
    elif nj_nw < 19231:
        jwh = ((nj_nw - 2885)  * -0.070) - 113
    elif nj_nw < 38462:
        jwh = ((nj_nw - 19231)  * -0.099) - 1257
    else:
        jwh = ((nj_nw - 38462)  * -0.118) - 3161

    jwh = round(jwh, 2)
    return jwh

class fcflowListView(ListView):
    model=fcflow
    template_name = "proj_1/list.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        qs=super().get_queryset(**kwargs)
        t = 0
        for i in qs:
            t += i.get_ann_amt()
        context['t_a'] = t
        context['t_m'] = round(t/12,2)
        context['t_b'] = round(t/26,2)
        context['t_w'] = round(t/52,2)
        context['t_d'] = round(t/365,2)

        return context

class fcflowDetailView(DetailView):
    model=fcflow
    template_name = "proj_1/detail.html"

class fcflowCreateView(CreateView):
    model=fcflow
    fields=["desc", "ann_freq", "amount"]
    template_name = "proj_1/fcflow_form.html"

class fcflowUpdateView(UpdateView):
    model=fcflow
    fields=["desc", "ann_freq", "amount"]

class fcflowDeleteView(DeleteView):
    model=fcflow
    template_name = "proj_1/fcflow_confirm_delete.html"
    success_url  = reverse_lazy("proj:list")

def withholding(request):
    template = 'proj_1/withholding.html'
    context = {}

    context['a_salary']=224000
    context['t_401k_pct']=-0.03
    context['r_401k_pct']=-0.02

    context['b_salary'] = round(context['a_salary']/26, 2)

    context['b_trad_401k'] = round(context['b_salary'] * context['t_401k_pct'], 2)
    context['b_post_t401k'] = round(context['b_salary'] + context['b_trad_401k'], 2)

    context['b_med']=-285.42
    context['b_dental']=-21.42
    context['b_vision']=-5.88
    context['m_transit']=-330

    context['pre_tax_exp'] = round(sum([context['b_med'], context['b_dental'], context['b_vision']]),2)

    context['b_fed_taxable'] = round(sum([context['b_salary'], context['pre_tax_exp'], context['b_trad_401k']]), 2)
    context['b_med_taxable'] = context['b_salary'] + context['pre_tax_exp']

    context['b_fed_taxable_t'] = round(context['b_fed_taxable'] + context['m_transit'], 2)
    context['b_med_taxable_t'] = round(context['b_med_taxable'] + context['m_transit'], 2)
    context['b_nj_taxable_t'] = round(context['b_post_t401k'] + context['m_transit'], 2)

    context['med_rate'] = -0.0145
    context['med_tax'] = round(context['b_med_taxable'] * context['med_rate'], 2)
    context['med_tax_t'] = round(context['b_med_taxable_t'] * context['med_rate'], 2)

    context['ss_tax_rate'] = -0.062
    context['ss_tax'] = round(context['b_med_taxable'] * context['ss_tax_rate'], 2)
    context['ss_tax_t'] = round(context['b_med_taxable_t'] * context['ss_tax_rate'], 2)

    context['b_fed_wh'] = get_fed_wh(context['b_fed_taxable'], -100)
    context['b_fed_wh_t'] = get_fed_wh(context['b_fed_taxable_t'], -100)

    context['fed_tax_rate'] = round(context['b_fed_wh']/context['b_fed_taxable'], 2)
    context['fed_tax_rate_t'] = round(context['b_fed_wh_t']/context['b_fed_taxable_t'], 2)

    context['b_ny_wh'] = get_ny_wh(context['b_fed_taxable'])
    context['b_ny_wh_t'] = get_ny_wh(context['b_fed_taxable_t'])

    context['ny_tax_rate'] = round(context['b_ny_wh']/context['b_fed_taxable'], 2)
    context['ny_tax_rate_t'] = round(context['b_ny_wh_t']/context['b_fed_taxable_t'], 2)

    context['ny_sdi_wh'] = -1.20

    context['nj_tax_rate'] = round(get_nj_wh(context['b_post_t401k'])/context['b_post_t401k'] , 2)
    context['nj_tax_rate_t'] = round(get_nj_wh(context['b_nj_taxable_t'])/context['b_nj_taxable_t'] , 2)

    context['b_nj_wh'] = round(get_nj_wh(context['b_post_t401k'])-context['b_ny_wh'], 2)
    context['b_nj_wh_t'] = round(get_nj_wh(context['b_nj_taxable_t'])-context['b_ny_wh_t'], 2)

    context['b_taxes'] = round(context['med_tax']+context['ss_tax']+context['b_fed_wh']+context['b_ny_wh']+context['ny_sdi_wh']+context['b_nj_wh'], 2)
    context['b_taxes_t'] = round(context['med_tax_t']+context['ss_tax_t']+context['b_fed_wh_t']+context['b_ny_wh_t']+context['ny_sdi_wh']+context['b_nj_wh_t'], 2)

    context['b_r_401k'] = round(context['b_salary'] * context['r_401k_pct'], 2)

    context['b_life'] = -32.29

    context['b_legal'] = -7.6

    context['post_tax'] = context['b_r_401k'] + context['b_life'] + context['b_legal']

    context['b_net_pay'] = round(sum([context['b_salary'], context['b_trad_401k'], context['pre_tax_exp'], context['b_taxes'], context['post_tax']]),2)

    context['d_net_pay'] = round(context['b_net_pay']/14,2)
    context['w_net_pay'] = round(context['b_net_pay']/2,2)
    context['a_net_pay'] = round(context['b_net_pay']*26,2)
    context['m_net_pay'] = round(context['a_net_pay']/12,2)

    context['b_net_pay_t'] = round(sum([context['b_salary'], context['b_trad_401k'], context['pre_tax_exp'], context['m_transit'], context['b_taxes_t'], context['post_tax']]),2)

    context['d_net_pay_t'] = round(context['b_net_pay_t']/14,2)
    context['w_net_pay_t'] = round(context['b_net_pay_t']/2,2)
    context['a_net_pay_t'] = round(context['b_net_pay_t']*26,2)
    context['m_net_pay_t'] = round(context['a_net_pay_t']/12,2)

    context['a_bonus'] = 21000 + 78750

    context['a_gross'] = context['a_salary'] + context['a_bonus']

    context['a_r_401k'] = context['r_401k_pct'] * context['a_gross']

    limit_401k = -23000

    context['a_t_401k'] = limit_401k-context['a_r_401k']

    context['a_transit'] = context['m_transit']*12

    a_nj_taxable = context['a_gross']+context['a_t_401k']
    context['a_med']= 26*context['b_med']
    context['a_den']= 26*context['b_dental']
    context['a_vis']= 26*context['b_vision']

    context['a_pre_tax_exp'] = sum([context['a_med'], context['a_den'], context['a_vis'], context['a_transit']])
    context['a_taxable'] = a_nj_taxable + context['a_pre_tax_exp']
    a_med_taxable = context['a_gross']+context['a_pre_tax_exp']
    a_exmed_taxable = a_med_taxable - 250000
    context['a_ss'] = 168600 * -0.062
    context['a_med_tax'] = (a_med_taxable*-0.0145)+(a_exmed_taxable*-0.009)
    context['a_ny_pfl'] = -333.25

    fed_std_ded = 27700
    #nj_exempt = 5000
    #nj_prop_tax = 18854

    fed_txbl = context['a_taxable']-fed_std_ded
    context['a_fed_tax'] = get_fed_tax(fed_txbl)

    context['a_ny_tax'] = get_ny_tax(context['a_taxable'])

    #nj_txbl = a_nj_taxable - nj_exempt-nj_prop_tax

    context['a_life']= 26*context['b_life']
    context['a_legal']= 26*context['b_legal']
    context['a_net']= sum([context['a_gross'], context['a_r_401k'], context['a_t_401k'], context['a_pre_tax_exp'], context['a_ss'], context['a_med_tax'], context['a_ny_pfl'], context['a_fed_tax'],  context['a_ny_tax'], context['a_life'], context['a_legal']])

    return render(request, template, context)