import sys
import os
import re

params_file = sys.argv[1] ##params file name jump_PT_ms2.params


def parserParams(filename):
  var_dict = {}
  with open(filename,"r") as f:
    for line in f:
      if line.strip():
        if line.startswith("#") == False:
          wanted_line = line.strip()
          if "#" in wanted_line:
            wanted_line_str = wanted_line.split("#")[0]
            key = wanted_line_str.split("=")[0].strip()
            value = wanted_line_str.split("=")[1].strip()
            var_dict[key] = value
         
          else:
            key = wanted_line.split("=")[0].strip()
            value = wanted_line.split("=")[1].strip()
            var_dict[key] = value
  return var_dict

d1 = parserParams(params_file)

params_dict={}
for key in d1.keys():
  print(key,d1[key])
  

  
 
