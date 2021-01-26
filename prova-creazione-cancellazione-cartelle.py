import yaml, os, shutil

#os.makedirs("oscar/marinetti", exist_ok=True)
#os.rmdir
#shutil.rmtree("oscar", ignore_errors=True)
"""
list = [{"name" : "pello"}, {"name" : "mello"}]
dict = {"patches" : list}
print(dict)
if "patches" in dict.keys():
  dict["patches"].clear()

print(dict)

open("patatoso", "x")
open("patatoso")
"""
list = []
ele1 = {"name" : "albio", "value" : "balbio"}
ele2 = {"name" : "blbio", "value" : "balbio"}
ele3 = {"name" : "nabbio", "value" : "balbio"}
list = [ele1, ele2, ele3]
for ele in list:
  print(ele["name"])

if "albio" in list