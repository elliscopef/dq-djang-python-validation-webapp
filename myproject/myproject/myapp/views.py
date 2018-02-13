# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
from resource.LibraryFile import simpleHTTPServerWithUpload

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            print(request.FILES['docfile'])
            #handle the validation of the newly loaded file
            #fn = os.path.join(path, fn[0])
            simpleHTTPServerWithUpload.validateCsvFile("/Users/mifang/Documents/Expedia/Project/tutorial/marginVali/ede_marginfile_validation_python/LibraryFile/Rev_GP_by_POS_FY18_201801_3PPackage_update.csv",1)
            #simpleHTTPServerWithUpload.validateCsvFile("/Users/mifang/Documents/Expedia/Project/tutorial/djangoTutorial/dq-djang-python-validation-webapp/myproject/myproject/myapp/resource/DataFile/sample3.0.csv",3)
            #navigation to a validation log page

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )

def log(request):
    return HttpResponseRedirect(reverse('log')) 
