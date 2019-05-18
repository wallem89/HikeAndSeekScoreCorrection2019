import urllib.request
import json

# Get overview off all total scores per group and filter on Seeker/Hiker
urlOverview = "https://dashboard.hikeandseek.nl/api/Archive/2019/Scores"
x = urllib.request.urlopen(urlOverview)
jdata = str(x.read().decode('utf-8'))
overallInfo = json.loads(jdata)
#print(overallInfo)

GroupNo = []
GroupPointOrg = []
GroupName = []
noOfSeekers = 0
for groupType in overallInfo:
    if groupType["participantType"] == "Seeker":
        noOfSeekers = noOfSeekers + 1
        GroupNo.append(str(groupType["number"]))
        GroupPointOrg.append(int(groupType["seekerPoints"] + groupType["extraPoints"]))
        GroupName.append(str(groupType["name"]))
print("Number of Seeker groups: ", noOfSeekers)

GroupCompensation = []
GroupPointNew = []
for group in GroupNo:
    # Get for each hiker group minus point and compensate
    url = "https://dashboard.hikeandseek.nl/api/Archive/2019/" + group + "/Points"
    x = urllib.request.urlopen(url)
    jdata = str(x.read().decode('utf-8'))
    groupInfo = json.loads(jdata)
    groupIndex = GroupNo.index(group)
    amountOf1Hints = 0;
    amountOf4Hints = 0;
    for infoRow in groupInfo:
        if infoRow["amountOfPoints"] == -75:
            infoRow["amountOfPoints"] = -15
            amountOf4Hints = amountOf4Hints + 1
        if infoRow["amountOfPoints"] == -25:
            infoRow["amountOfPoints"] = -5
            amountOf1Hints = amountOf1Hints + 1
    GroupCompensation.append(amountOf1Hints * 20 + amountOf4Hints * 60)
    GroupPointNew.append(GroupPointOrg[groupIndex] + GroupCompensation[groupIndex])
    #print("Group number: ", group)
    #print("Group name: ", GroupName[groupIndex])
    #print("Number of 1 hint bought: ", amountOf1Hints)
    #print("Number of 4 hints bought: ", amountOf4Hints)
    #print("Original number of points: ", GroupPointOrg[groupIndex])
    #print("Total amount of hint compensation: ", GroupCompensation[groupIndex])
    #print("New number of points: ", GroupPointNew[groupIndex])

# Sort list of Group points to get new score
def sort_list(list1, list2):

    zipped_pairs = zip(list2, list1)

    y = [x for _, x in sorted(zipped_pairs)]
    z = y[::-1]
    return z

sortedGroupNameOrg = sort_list(GroupName, GroupPointOrg)
sortedGroupNameNew = sort_list(GroupName, GroupPointNew)
sortedGroupNoOrg = sort_list(GroupNo, GroupPointOrg)
sortedGroupNoNew = sort_list(GroupNo, GroupPointNew)
sortedGroupPointOrg = sort_list(GroupPointOrg, GroupPointOrg)
sortedGroupPointOld = sort_list(GroupPointOrg, GroupPointNew)
sortedGroupPointNew = sort_list(GroupPointNew, GroupPointNew)
#print(sortedListOrg)
#print(sortedListNew)



#Write output to file
f=open("C:/Users/Admin/Desktop/HikeAndSeekResult2019.txt","w+")
f.write("Original Seeker score 2019:\n")
f.write("Number, Team, Name, Score\n")
for i in sortedGroupNameOrg:
    index = sortedGroupNameOrg.index(i)
    string = str(index + 1) + ", " + str(sortedGroupNoOrg[index]) + ", " + str(sortedGroupNameOrg[index] ) + ", " + str(sortedGroupPointOrg[index])
    f.write(string + "\n")
f.write("Corrected Seeker score 2019:\n")
f.write("Number, Team, Name, Score old, Score new\n")
for i in sortedGroupNameNew:
    index = sortedGroupNameNew.index(i)
    string = str(index + 1) + ", " + str(sortedGroupNoNew[index]) + ", " + str(sortedGroupNameNew[index] ) + ", " + str(sortedGroupPointOld[index]) + ", " + str(sortedGroupPointNew[index])
    f.write(string + "\n")
f.close()