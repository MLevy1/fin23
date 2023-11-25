from django.shortcuts import render

from .forms import Moving

import numpy_financial as npf

def move(response):
  if response.method=="POST":
    result=response.POST

    irate = float(result.get("irate"))
    term = float(result.get("term"))
    pprice = float(result.get("purchprice"))
    dpp = float(result.get("dppct"))/100

    dpa = pprice*dpp

    pv = pprice-dpa

    mrate = (irate/12) / 100
    nper = term*12
    
    mtg = npf.pmt(mrate, nper, pv, fv=0)
    mins = -1*float(result.get("annins"))/12

    ptr = float(result.get("ptaxrate"))/100
    mpt = -1*(ptr*pprice)/12

    tmpmt=mtg+mins+mpt

    result = {"tmpmt": tmpmt, "mpt": mpt, "mins": mins, "mtg": mtg, "dpa":dpa, "pprice": pprice }

    return render(response, "moving/movecalcs.html", {"result":result})

  else:
    form = Moving(initial={"irate": 6.15, "term": 30, "ptaxrate": 1.813, "annins": 4000, "purchprice": 1210000, "dppct": 20 })

  return render(response, "moving/move.html", {"form":form})