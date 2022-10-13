from math import ceil
import os
os.chdir("D:/")  # we set the directory from where to read the file
import pandas as pa
import numpy as np

TAPref = pa.read_csv('TA preferences.csv')  # importing a csv file
facultyPref = pa.read_csv('Faculty preferences.csv',usecols=["Course no.", "Total TA count"])

facultyPref = facultyPref[facultyPref["Course no."]<"CS601"]   # took only UG courses from the data

facultyPref["Total TA count"] = (facultyPref["Total TA count"]/2).apply(np.ceil)  # divided the Total TA count by 2 for Mtech1 students

print(sum(facultyPref['Total TA count']))  # Total Mtech1 TA needed in the UG courses 

TAPref = TAPref[TAPref["Batch"]<"Phd"]    # took preferences of only Mtech students for the allocation

TA_dict = {}
pref = ['Preference 1','Preference 2','Preference 3','Preference 4','Preference 5','Preference 6','Preference 7','Preference 8']   # no of preferences filled

for i in range(len(TAPref)):     # this function is used to make a dictionary "TA_dict" mapping TA with their preferences
    
    for j in pref:
        if TAPref[j][i]<"CS601":
            if TAPref['ID'][i] in TA_dict:
                TA_dict[TAPref['ID'][i]].append(TAPref[j][i])
                
            else:
                TA_dict[TAPref['ID'][i]] = []
                TA_dict[TAPref['ID'][i]].append(TAPref[j][i])


matching = {}
    
for i in range(len(facultyPref)):                            # this function is used to make a dictionary "matching" storing matching edges
    for j in range(int(facultyPref['Total TA count'][i])):
        if facultyPref["Course no."][i] in matching:
            matching[facultyPref['Course no.'][i]].append(-1)
        else:
            matching[facultyPref['Course no.'][i]] = []
            matching[facultyPref['Course no.'][i]].append(-1)
 

def visited_dict(facultyPref):                         # this function is used to make a dictionary of visited courses initialized with zero(not visited)
    visited = {}
    for i in range(len(facultyPref)):
        for j in range(int(facultyPref['Total TA count'][i])):
            if facultyPref["Course no."][i] in visited:
                visited[facultyPref['Course no.'][i]].append(0)
            else:
                visited[facultyPref['Course no.'][i]] = []
                visited[facultyPref['Course no.'][i]].append(0)
    return visited
               

def bipartiteMatch(interested,applicant,visited,matching):
    
    for course in interested[applicant]:     # traversing for all the preferred courses of that TA 
        
        if course in visited:       
            for i in range(len(visited[course])):   # traversing for all the spaces of that course
                
                if visited[course][i]==0:         # checking if that space of the course is already visited or not
                    visited[course][i] = 1        # if not visited then marking it as visited
                    
                    if (matching[course][i]<0 or bipartiteMatch(interested,matching[course][i],visited,matching)):   # checking if that space of the course is already
                        matching[course][i] = applicant                                                              # matched to some other applicant or not:
                        return True                                                                                  # if not matched - then allocate that space to him
                                                                                                                     # if matched - check whether the applicant already
                                                                                                                     # matched can be allocated to some other course,
                                                                                                                     # if we can allocate that applicant with some other
                                                                                                                     # course, then we can match our applicant with this
                                                                                                                     # course.
                                                                                                                     # also when we are checking to allocate some other
                                                                                                                     # course to that applicant he will not visit the 
                                                                                                                     # same course as it is already marked as visited
    return False

unmatched = []   # storing the unmatched TAs in a list

def maxBipartiteMatch(TA_dict,matching):          # returns the number of students assigned to courses 
    
    ans = 0                                # storing the count of number of TAs allocated
    
    for applicant in TA_dict:              # running this loop for each TA in TA_dict
       
        visited = visited_dict(facultyPref)      # creating a visited dictionary for each TA
        
        if bipartiteMatch(TA_dict,applicant,visited,matching):    # calling this function to see whether this TA can be allocated to some course or not
            ans+=1
        else:
            unmatched.append(applicant)    # appending the TA id to the unmatched list
    
    return ans
        

print(maxBipartiteMatch(TA_dict,matching))

# df = pa.DataFrame.from_dict(matching, orient='index')
# df = df.transpose()
# # This writes to output.csv
# df.to_csv("output.csv", index = False)       # storing the mapping of allocated TAs with their course in a csv file
