from django.db import models

# Create your models here.
# class ScientistInfo(models.Model):
#     University=models.CharField(max_length=500)
#     NqfLevel=models.IntegerField()
#     QualificationName=models.CharField(max_length=500)
#     Industry=models.CharField(max_length=500)
#     WorkedExperience=models.IntegerField()
#     EvalResults=models.BooleanField()

#     def EvaluateScientist(self):

#         return self.EvalResults
    
class Universities(models.Model):        
    UniversityName = models.CharField(max_length=500)  
    def __str__(self):
        return self.UniversityName 
       
    class Qualifications(models.Model):           
        QualificationsName=models.CharField(max_length=500)
        def ___str__ (self):
             return self.QualificationsName
        
    # class Result(models.Model):        
    #         Result=models.BooleanField()
    #         def str (self):
    #          return self.UniversityName