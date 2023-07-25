#author: siayouyang
#version: relion_model_20230725
#put this script inside the folder containing Relion "*_model.star" files
#execute: python relion_model_xyy.py
#results: only "class distribution" and "estimated resolution" are exported (model_classDist_stats.txt & model_estRes_stats.txt

import re
import os

#get all _model.star files without repeated
current_dir = "."
dir = os.listdir(current_dir)

model_star_list = []
file_index_list = []
for file in dir:
    matchObj = re.search(r"_model.star", file)
    if matchObj:
        file_index = file[-14:-11]
        if file_index not in file_index_list:
            model_star_list.append(file)
            file_index_list.append(file_index)

#sort _model.star files according to num of iteration
def getNumIt(filename):
    return filename[-14:-11]

model_star_list.sort(key=getNumIt)

#get info of class distribution and estimated resolution to dict
dict = {}
num_of_iters = -1
for model_star in model_star_list:
    input = open(model_star, 'r')
    n = 0
    num_of_classes = 0
    for line in input.readlines():
        if line == "\n" and n <= 3:
            n+=1
        elif n > 3:
            #print(line)
            if re.search(r"_rlnReferenceImage", line):
                a = int(line[-3]) - 1
            elif re.search(r"_rlnClassDistribution", line):
                b = int(line[-3]) - 1
            elif re.search(r"_rlnEstimatedResolution", line):
                c = int(line[-3]) - 1
            elif re.search(r"Class3D/", line):
                num_of_classes += 1
                r_iteration = line.split()[a][-16:-13].lstrip("0")
                if r_iteration == "":
                    r_iteration = 0
                r_class = (line.split()[a][-7:-4]).lstrip("0")
                it_class = str(r_iteration) + "_" + str(r_class)
                dict.update({it_class: {"classDist": line.split()[b], "estRes": line.split()[c]}})
            elif line == "\n":
                num_of_iters += 1
                break

#save to txt file
classDist_output = open("model_classDist_stats.txt", 'w')
classDist_output.write("iters" + "\t")
for classes in range(1, num_of_classes+1):
    classDist_output.write(str(classes) + "\t")
classDist_output.write("\n")
for iters in range(0, num_of_iters+1):
    classDist_output.write(str(iters) + "\t")
    for classes in range(1, num_of_classes+1):
        it_class = str(iters) + "_" + str(classes)
        class_dist = dict[it_class]["classDist"]
        classDist_output.write(str(class_dist) + "\t")
    classDist_output.write("\n")
classDist_output.close()

estRes_output = open("model_estRes_stats.txt", 'w')
estRes_output.write("iters" + "\t")
for classes in range(1, num_of_classes+1):
    estRes_output.write(str(classes) + "\t")
estRes_output.write("\n")
for iters in range(0, num_of_iters+1):
    estRes_output.write(str(iters) + "\t")
    for classes in range(1, num_of_classes+1):
        it_class = str(iters) + "_" + str(classes)
        est_res = dict[it_class]["estRes"]
        estRes_output.write(str(est_res) + "\t")
    estRes_output.write("\n")
estRes_output.close()

print("done!")