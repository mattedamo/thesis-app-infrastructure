import yaml, os

def main():
  
  tier = "backend"
  
  

  imageTagFrontend = ""
  with open("./prova.yaml") as file:
    input = yaml.load(file, Loader=yaml.FullLoader)
  if input["image"]["frontend"]["tag"]
  for k,v in input.items():
    if k == "image":
      if input["image"].keys() != None and "frontend" in input["image"].keys():
        if input["image"]["frontend"].keys() != None and "tag" in input["image"]["frontend"].keys():
          imageTagFrontend = input["image"]["frontend"]["tag"]
  if imageTagFrontend == "":
    print("none")
  else:
    print(imageTagFrontend)

  
if __name__ == '__main__':
    main()
