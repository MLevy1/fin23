from django.shortcuts import (
	render,
	get_object_or_404,
	redirect,
	Http404,
)

from django.http import HttpResponse

from django.urls import (
	reverse
)

from .models import (
    Flow,
    FlowItem,

)

from .forms import (
    FlowForm,
    FlowItemForm,

)

#F1
def flow_list_view(request):
    qs = Flow.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "fixed/list.html", context)

#F4
def flow_detail_view(request, id=None):
    obj = get_object_or_404(Flow, id=id)
    context = {
        "object": obj
    }
    return render(request, "fixed/detail.html", context)

#F2
def flow_create_view(request):
    form = FlowForm(request.POST or None)

    template = "fixed/create-update.html"

    context = {
        "form": form
    }

    if form.is_valid():
        obj = form.save()
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_edit_url()
            }
            return HttpResponse("created!", headers=headers)

        return redirect(obj.get_edit_url())

    return render(request, template, context)

#F3
def flow_update_view(request, id=None):
    obj = get_object_or_404(Flow, id=id)

    form = FlowForm(request.POST or None, instance=obj)

    new_item_url = reverse("fixed:item_create_hx", kwargs={"parent_id": obj.id})

    template = "fixed/create-update.html"

    context = {
        "form": form,
        "object": obj,
        "new_item_url": new_item_url,
    }

    if form.is_valid():
        form.save()
        context['message'] = "saved!"

        if request.htmx:
            return render(request, "fixed/partials/form.html", context)

    return render(request, template, context)

#F5
def flow_item_update_hx_view(request, parent_id=None, id=None):

    #if the request is not an htmx request, it's unauthorized > end of view
    if not request.htmx:
        raise Http404

    #this block ensures that a parent object (the paycheck that the paycheck line items will be attached to exists. if it doesn't > end of view

    try:
        parent_obj = Flow.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not Found")

    #at this point, it has been confirmed that a parent_object exists

    #instance is set to "none" assuming that no instances exist
    instance = None

    #if an id has been passed to the view it means that an instance does exist and can be retrieved
    if id is not None:
        try:
            instance = FlowItem.objects.get(flow=parent_id, id=id)
        except:
            instance = None

    #this will return an empty form if a paycheck item that doesn't exist is passed to the view

    form = FlowItemForm(request.POST or None, instance=instance)

    url = instance.get_hx_edit_url() if instance else reverse("fixed:item_create_hx", kwargs={"parent_id": parent_obj.id})

    context = {
        "url": url,
        "form": form,
        "object": instance,
    }


    if form.is_valid():

        #the form is saved without committing in case there is no instance
        new_obj = form.save(commit=False)

        #if there is no instance, the paycheck is set to the parent_object
        if instance is None:
            new_obj.flow = parent_obj

        #then the form is saved with committing
        new_obj.save()
        context['object'] = new_obj
        return render(request, "fixed/partials/item-inline.html", context)

    return render(request, "fixed/partials/item-form.html", context)

#F6
def flow_delete_view(request, id=None):

    try:
        obj = Flow.objects.get(id=id)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404

    if request.method == "POST":
        obj.delete()
        success_url = reverse("fixed:list")

        if request.htmx:
            headers = {
    			'HX-Redirect': success_url
    		}
            return HttpResponse("Deleted", headers=headers)
        return redirect(success_url)

    template = "fixed/delete.html"

    context = {
	    "object": obj
    }

    return render(request, template, context)

#F7
def item_delete_view(request, parent_id=None, id=None):

    try:
        obj = FlowItem.objects.get(id=id, flow_id=parent_id)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404

    if request.method == "POST":
        obj.delete()
        success_url = reverse("fixed:update", kwargs={'id': parent_id })

        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Deleted", headers=headers)
        return redirect(success_url)

    template = "fixed/delete.html"

    context = {
        "object": obj
    }

    return render(request, template, context)