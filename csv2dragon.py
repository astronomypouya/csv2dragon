#!/usr/bin/python
import csv

#inputs
file_name = "Voice commands csv - dot2.csv"


# find number of groups
group_list = []
last_group = ""
row_number = 1
print("group types are ")
with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    number_of_groups = -1

    for row in csv_reader:
        if row_number == 1:
            if row[0] != 'Group' or row[1] != 'Voice command' or row[2] != 'Type' \
                or row[3] != 'Code' or row[4] != 'Comments':
                Exception("Column entries are incorrect.")
                exit()
        row_number += 1

        if last_group != row[0] and row[0] != '':
            group_list.append(row[0])
            if row[0] != group_list[0]:
                print("\t " + row[0])
            number_of_groups += 1
            last_group = row[0]
csv_file.close()

if len(group_list) == 0:
    exit()
    
fw = open(group_list[1] + ".gr.dra.txt", "w")
fw_arg = open(group_list[1] + ".arg.dra.txt", "w")
last_group = group_list[1]
fw.write("Sub Main\n\n")
command_count = 0


with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        group = row[0]
        voice_command = row[1]
        code_type = row[2]
        code = row[3]
        comment = row[4]

        if group == group_list[0]:
            continue


        if group != last_group and group != '':
            fw.write("\tEnd If\n\n")
            fw.write("End Sub")
            fw.close()
            fw_arg.close()
            fw = open(group + ".gr.dra.txt", "w")
            command_count = 0
            fw.write("Sub Main\n\n")
            last_group = group

        splt = voice_command.split()
        if len(splt) == 0:
            continue
        
        start_ind = 0
        end_ind = len(voice_command) 
        #finding the start of command args
        if splt[0] == group:
            start_ind = len(group)+1
        #finding the end of command args
        for ind in range(0, len(voice_command)):
            if voice_command[ind] == '<':
                if ind == 0:
                    end_ind = ind
                    break
                else:
                    end_ind = ind - 1
                    break
        #seetting command args
        voice_command = voice_command[start_ind:end_ind]

        fw_arg.write(voice_command + "\n")

        if command_count == 0:
            fw.write("\tIf ListVar1 = \"" + voice_command +"\" Then \n")
        else:
            fw.write("\tElseIf ListVar1 = \"" + voice_command +"\" Then \n")
            
        command_count = command_count + 1
        if code_type == 'dragonkeys':
            fw.write("\t\tSendDragonKeys \"" + code + "\"")
            fw.write(" '" + comment.replace("\n", "%") + "\n")
        elif code_type == 'code':
            fw.write("\t\t" + comment.replace("\n", "%") + "\n" + code.replace("Sub Main", "").replace("End Sub","").replace("\n", "\n\t\t") + "\n")
            fw.write("\t '" + comment.replace("\n", "%") + "\n")
        else:
            fw.write("\t\tSendKeys \"" + code + "\"")
            fw.write(" '" + comment.replace("\n", "%") + "\n")
        fw.write("\n")
        
fw.write("\tEnd If\n\n")
fw.write("End Sub")
fw_arg.close()
fw.close()


        