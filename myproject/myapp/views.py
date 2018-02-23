# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
from resource.LibraryFile import simpleHTTPServerWithUpload
from resource import validateMarginFile
from resource import varSettings
import os

global logInfo 
global ValidationIndex

logInfo = []


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            print("Retrive the uploaded file")
            dirTwoLevelUp = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'media/documents'))
            addSlashToFile = '/'+request.FILES['docfile'].name
            uploadedFileAbsPath = os.path.join(dirTwoLevelUp,request.FILES['docfile'].name)


            print("uploadedFileAbsPath  : ")
            print(uploadedFileAbsPath)
            
            print("fileFormatSelection: ")
            print(request.POST['fileFormatSelection'])

            if (request.POST['fileFormatSelection']=='M_V_1'):
                ValidationIndex = 1;
            else:
                ValidationIndex = 3;
            

            print("Start the validation process")
            validateMarginFile.validateMarginFileProcess(uploadedFileAbsPath,ValidationIndex,logInfo)
            # validateMarginFile.validateMarginFileProcess("/Users/mifang/Documents/Expedia/Project/tutorial/djangoTutorial/dq-djang-python-validation-webapp/myproject/myproject/myapp/resource/DataFile/sample3.0.csv",3,logInfo)
            
            
            print("Start to remove the file from the folder")
            os.remove(uploadedFileAbsPath)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('log'))
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
    return render(
        request,
        'log.html',
        {'documents': logInfo}
    )

