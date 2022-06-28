from cProfile import label
from email.policy import default
from hashlib import new
import attr
from django.urls import reverse
from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict


from random import randrange
from django.shortcuts import render

from . import util
from . import convert
import encyclopedia


class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label = "Title")
    MD_content =  forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}), label ="Markdown content")
  
   


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)    
        if form.is_valid():
            if form.cleaned_data["entry_title"] in util.list_entries():
                return render (request, "encyclopedia/error.html",{
                 "error_message":"Entry for " + form.cleaned_data["entry_title"] +" already exists!"})
            else:
                content = "# "+ form.cleaned_data["entry_title"] +"\n"+form.cleaned_data["MD_content"]
                util.save_entry(form.cleaned_data["entry_title"],content)
                return entry(request,form.cleaned_data["entry_title"])
    else:
        return render (request,"encyclopedia/addentry.html",{
        "form":NewEntryForm()})



def edit(request):
    qd =QueryDict()
    qd = request.GET
    form = NewEntryForm(initial={'entry_title' : qd["title"],
    'MD_content': util.get_entry(qd["title"])
    })
    return render (request, "encyclopedia/editentry.html",{
        "form": form})



def edit_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)    
        if form.is_valid():
                util.save_entry(form.cleaned_data["entry_title"], form.cleaned_data["MD_content"])
                return entry(request,form.cleaned_data["entry_title"])
    else:
        return render (request,"encyclopedia/addentry.html",{
        "form":NewEntryForm()})



def search(request):
    entries = util.list_entries()
    new_entries =[]
    qd =QueryDict()
    qd = request.GET
    search_query =""
    search_query = qd["q"]

    if search_query in entries:
         return entry(request, search_query)
    else:
        for e in entries:
            if search_query in e:
                new_entries.append(e)

    if len(new_entries)>0:
        return render(request, "encyclopedia/index.html", {
        "entries": new_entries
    })
    else:
        return render (request,"encyclopedia/error.html",{
        "error_message":"Entry for " + search_query +" does not exists!"})
    
    

def random_entry(request):
    entries = util.list_entries()
    i = randrange(0,len(entries)-1)
    return entry(request, entries[i])


def entry(request, title):
    entry_md =  util.get_entry(title)
    if entry_md is None:
        return render (request,"encyclopedia/error.html",{
            "error_message":"Entry does NOT exist!"})
    else:
        entry_html = convert.convertMDtoHTML(entry_md)
        return render (request,"encyclopedia/entry.html",{
            "entry_title":title, "entry_html":entry_html
        })
