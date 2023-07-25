#author: siayouyang
#version: relion_particles_per_micro_20230725
#put this script inside the folder(eg. Refine3D/job???/) containing Relion "run_data.star" files
#WARNING: "Images" folder name must be unique if particles are from different batch of images data, otherwise images index will be confused.
#execute: python relion_particles_per_micro_xyy.py
#results: particles_per_micro_stats.txt
#postprocess using Microsoft Excel

from collections import Counter

input = open("run_data.star", 'r')
list = []
for a in input:
    if not a.startswith("_") and not a.endswith("_ \n") and not a.endswith("_\n") and a != "" and a !="\n" and a !=" \n":
        b = a.split("stack_")[1]
        c = b.split("_cor2")[0]
        d = int(c.lstrip("0"))
        i = a.split("/stack_")[0]
        images = i.split("/")[-1]
        list.append(str(images) + "::" + str(d))
input.close()

list.sort()
dict = Counter(list)
output = open("particles_per_micro_stats.txt", 'w')

for a in dict:
    images = a.split("::")[0]
    index = a.split("::")[1]
    b = int(index)
    output.write(str(images) + ":" + str(b) + " " + str(dict[a]) + "\n")

output.close()
print("done")