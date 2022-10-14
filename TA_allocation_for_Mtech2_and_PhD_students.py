
from math import ceil, factorial
import os
import queue

os.chdir("D:/")  # we set the directory from where to read the file
import pandas as pa
import numpy as np

TAPref = pa.read_csv('TA preferences.csv')  # importing a csv file
facultyPref = pa.read_csv('Mtech2.csv')

print(sum(facultyPref['Mtech 2 TA count']))  # Number of Mtech2 TAs needed for the courses
TAPref = TAPref.astype('str')
TAPref = TAPref[TAPref["Batch"]<"Phd"]    # took preferences of only Mtech2 students for the allocation
facultyPref.fillna(0,inplace=True)
facultyPref = facultyPref.astype({'Mtech 2 TA count': int,'Preference 1': int,'Preference 2': int,'Preference 3': int,'Preference 4': int,'Preference 5': int,'Preference 6': int,'Preference 7': int,'Preference 8': int,'Preference 9': int,'Preference 10': int})
facultyPref = facultyPref.astype('str')

faculty_dict = {}
fpref = ['Preference 1','Preference 2','Preference 3','Preference 4','Preference 5','Preference 6','Preference 7','Preference 8','Preference 9','Preference 10']   # no of preferences filled

for i in range(len(facultyPref)):    # faculty_dict will store the preferences of Instructors
    
    for j in fpref:
        
        if facultyPref['Course no.'][i] in faculty_dict:
            if facultyPref[j][i] != '0':
                faculty_dict[facultyPref['Course no.'][i]].append(facultyPref[j][i])
            
        else:
            faculty_dict[facultyPref['Course no.'][i]] = []
            if facultyPref[j][i] != '0':
                faculty_dict[facultyPref['Course no.'][i]].append(facultyPref[j][i])

TAcnt = {}                   # it stores the number of Mtech2 TAs needed for each course
for i in range(len(facultyPref)):
    TAcnt[facultyPref['Course no.'][i]] = facultyPref['Mtech 2 TA count'][i]
    
pref = ['Preference 1','Preference 2','Preference 3','Preference 4','Preference 5','Preference 6','Preference 7','Preference 8']   # no of preferences filled

TA_dict = {}

for i in range(len(TAPref)):     # this function is used to make a dictionary "TA_dict" mapping TA with their preferences
    
    for j in pref:
        
        if TAPref['ID'][i] in TA_dict and TAPref[j][i] in faculty_dict:
            
            TA_dict[TAPref['ID'][i]].append(TAPref[j][i])
            
        elif TAPref['ID'][i] not in TA_dict:
            TA_dict[TAPref['ID'][i]] = []
            
            if TAPref[j][i] in faculty_dict:
                TA_dict[TAPref['ID'][i]].append(TAPref[j][i])
               


for applicant in TA_dict:                 # appending the applicant in the preference list of the course if it is not in the list 
    for course in TA_dict[applicant]:     # making our edge set symmetric
        if applicant not in faculty_dict[course]:
            faculty_dict[course].append(applicant)

 
for course in faculty_dict:          # appending course in the preference list of student if that course is not selected by the
    for applicant in faculty_dict[course]: #student and instructor has that student in his preference list, we will make this course
        if course not in TA_dict[applicant]:# the last preferred course for that student
            TA_dict[applicant].append(course)

k=2                              # using k layers in our algorithm

for i in range(len(TAPref)):     # making k copies of each applicant and appending the number of copies of each course equal to the
    for j in range(97,97+k):     # number of TAs needed for that course in the preference list
        TA_dict[TAPref['ID'][i] + chr(j)] = []
        for course in TA_dict[TAPref['ID'][i]]:
            for cnt in range(int(TAcnt[course])):
                TA_dict[TAPref['ID'][i] + chr(j)].append(course + '_' + str(cnt))
    
    del TA_dict[TAPref['ID'][i]]


for i in range(len(facultyPref)):        # making number of copies of each course equal to the number of TAs needed for the course
    for j in range(int(TAcnt[facultyPref['Course no.'][i]])): # with the same preference list for all the copies of that course
        faculty_dict[facultyPref['Course no.'][i] + '_' + str(j)] = faculty_dict[facultyPref['Course no.'][i]]
    
    del faculty_dict[facultyPref['Course no.'][i]]

fac_dict = {}
for course in faculty_dict:   # updating the preference list of each course
    list = []
    for j in range(97+k-1,96,-1):
        
        for applicant in faculty_dict[course]:
            list.append(applicant+chr(j))
    fac_dict[course] = list


def remove_items(test_list, item):
 
    # using list comprehension to perform the task
    res = [i for i in test_list if i != item]
 
    return res

matching = {}      # this will store the matching edges

q = queue.Queue()     # create a queue

for applicant in TA_dict:
    if applicant[len(applicant)-1]=='a':  # Initialize the queue with the bottom layer copies of all the students
        q.put(applicant)


while q.empty()==False:                   # main algorithm
    applicant = q.get()                   # get the student in the queue
    # print(applicant)
    if len(TA_dict[applicant]) != 0:
        preferredCourse = TA_dict[applicant][0]    # first preferred course of the student
        
        if preferredCourse in matching:          # if that course is already matched, put the matched student in the queue
            q.put(matching[preferredCourse])     
             
        matching[preferredCourse] = applicant    # match the student to the course as it prefers this student more than the current
                                                # matching because we have removed all the worse ranked neighbors after the course  
                                                # gets allocated to some student
        prefListOfCourse = fac_dict[preferredCourse]
        
        
        indx = prefListOfCourse.index(applicant)
        
        for i in range(indx+1,len(prefListOfCourse)):   # removing all the worse ranked neighbors
           
            TA_dict[prefListOfCourse[i]] =  remove_items(TA_dict[prefListOfCourse[i]],preferredCourse)
            
        prefListOfCourse = prefListOfCourse[0:indx+1]
       
        fac_dict[preferredCourse] = prefListOfCourse
        
    
    elif applicant[len(applicant)-1] < chr(97+k-1):   # if the student remains unmatched, then he is promoted to the next layer
        char = applicant[len(applicant)-1]
        app = applicant[:len(applicant)-1]
        app = app + chr(ord(char)+1)
        q.put(app)


for map in matching:
    applicant = matching[map]
    applicant = applicant[:len(applicant)-1]
    matching[map] = applicant
    
# df = pa.DataFrame.from_dict(matching, orient='index')
# df = df.transpose()
# df.to_csv("output.csv", index = False)

# analysis = {}
# for map in matching:
#     applicant = matching[map]
#     map  = map[0:len(map)-2]
#     analysis[applicant] = map
# print(len(analysis))
# pr = [0,1,2,3,4,5,6,7]
# cnt = {}
# for app in analysis:
#     if analysis[app] in TA_dict1[app]:
#         ind = TA_dict1[app].index(analysis[app])
#         if ind in cnt:
#             cnt[ind] +=1
#         else:
#             cnt[ind] = 1
        
#     else:
#         if 10 in cnt:
#             cnt[10] += 1
#         else:
#             cnt[10] = 1

# print(cnt)
    
# print(analysis)

