from django.shortcuts import render
import clr
import os
from System import Collections
from System.Collections.Generic import List

# Create your views here.
def check(request):
    return render(request, 'SACNASPregister.html', {})

def university_list(request):
    obj=PercentageComputation()
    university_folder = 'UniversityFiles\\'
    csv_files = [file for file in os.listdir(university_folder) if file.endswith('.csv')]
    # Convert the Python list to a List[string] object
    csv_files_list = List[str]()
    for file in csv_files:
        csv_files_list.Add(university_folder+file)
    #print(csv_files)  
    obj.setUniversuty(csv_files_list)
    universities=obj.getUniversities()

    context = {'universities': universities}
    for i in context:
        print(i)
    return render(request, 'SACNASPregister.html', context)


    
