import clr
import os
from System import Collections
from System.Collections.Generic import List

clr.AddReference("SACNASP_DATA")
from SACNASP_DATA import PercentageComputation

obj=PercentageComputation()
university_folder = 'UniversityFiles'
csv_files = [file for file in os.listdir(university_folder) if file.endswith('.csv')]

     
csv_files_list = List[str]()
for file in csv_files:
    csv_files_list.Add(file)
#print(csv_files)
print("===================Start :==================")

obj.setUniversuty(csv_files_list)

print("==================getUniversities Start====================")
universtyNames=obj.getQualifications()
print("==============getUniversities Done===========")
for name in universtyNames:
    print(name)


