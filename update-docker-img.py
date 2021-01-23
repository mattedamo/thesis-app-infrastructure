import yaml, os

def main():
  
  tier = os.environ["TIER"]
  code_branch = os.environ["CODE_BRANCH"]
  user_dockerhub = os.environ["DOCKER_USER"]
  
  repo_name_frontend_dockerhub = os.environ["DOCKER_FRONTEND_REPO"]
  repo_name_backend_dockerhub = os.environ["DOCKER_BACKEND_REPO"]
  image_tag = os.environ["DOCKER_TAG"]

  if "master" in code_branch:
    kustomization_path = "kustomize/overlays/prod/kustomization.yaml"
  else: 
    kustomization_path = "kustomize/overlays/"+tier+"/"+code_branch+"/kustomization.yaml"

  for filename in os.listdir("kustomize/base/"):
          with open(os.path.join("kustomize/base/", filename)) as file:
              f = yaml.load(file, Loader=yaml.FullLoader)
          if f["kind"] == "Deployment":
              if f["spec"]["template"]["metadata"]["labels"]["tier"] == "frontend":
                imageNameFrontend = f["spec"]["template"]["spec"]["containers"][0]["name"]
              elif f["spec"]["template"]["metadata"]["labels"]["tier"] == "backend":
                imageNameBackend = f["spec"]["template"]["spec"]["containers"][0]["name"]
  with open(kustomization_path) as file:
      kustomization = yaml.load(file, Loader=yaml.FullLoader)
  
  if "master" in code_branch:
    entryBackend = {"name" : imageNameBackend, "newName" : user_dockerhub+"/"+repo_name_backend_dockerhub, "newTag" : "latest-prod"}
    entryFrontend = {"name" : imageNameFrontend, "newName" : user_dockerhub+"/"+repo_name_frontend_dockerhub, "newTag" : "latest-prod"}

  
  else:

    if(tier == "backend"):
      entryBackend = {"name" : imageNameBackend, "newName" : user_dockerhub+"/"+repo_name_backend_dockerhub, "newTag" : image_tag}
      imageTagFrontend = None
      with open("./input.yaml") as file:
        input = yaml.load(file, Loader=yaml.FullLoader)
      for k,v in input.items():
        if k == "image":
          imageTagFrontend = input["image"]["frontend"]["tag"]
      if imageTagFrontend == None:
        imageTagFrontend = "latest-prod"
      entryFrontend = {"name" : imageNameFrontend, "newName" : user_dockerhub+"/"+repo_name_frontend_dockerhub, "newTag" : imageTagFrontend}


    elif (tier == "frontend"):
      entryFrontend = {"name" : imageNameFrontend, "newName" : user_dockerhub+"/"+repo_name_frontend_dockerhub, "newTag" : image_tag}
      imageTagBackend = None
      with open("./file.yaml") as file:
        input = yaml.load(file, Loader=yaml.FullLoader)
      for k,v in input.items():
        if k == "image":
          imageTagBackend = input["image"]["backend"]["tag"]
      if imageTagBackend == None:
        imageTagBackend = "latest-prod"
      entryBackend = {"name" : imageNameBackend, "newName" : user_dockerhub+"/"+repo_name_backend_dockerhub, "newTag" : imageTagBackend}

  if "images" not in kustomization.keys():
    kustomization["images"] = [entryBackend, entryFrontend]
    #aggiungo scrivendo, la key patch
    with open(kustomization_path, "w") as file:
        yaml.dump(kustomization, file)
  else:
    #vuol dire che la entry patch esiste, ma non è detto che esista nella sua lista, il list_value necessario
    foundBackend = False #inizializzo la variabile
    foundFrontend = False #inizializzo la variabile
    for e in kustomization["images"]:
        if e["name"] == imageNameFrontend:
          foundFrontend = True
          kustomization["images"].remove(e)
          kustomization["images"].append(entryFrontend)
        elif e["name"] == imageNameBackend:
          foundBackend = True
          kustomization["images"].remove(e)
          kustomization["images"].append(entryBackend)

    if foundBackend == False:
        kustomization["images"].append(entryBackend)
    if foundFrontend == False:
        kustomization["images"].append(entryFrontend)

    with open(kustomization_path, "w") as file:
        yaml.dump(kustomization, file)
      
if __name__ == '__main__':
    main()
