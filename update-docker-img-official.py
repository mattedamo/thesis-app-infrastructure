import yaml, os

def main():
  
  

  if "master" in os.environ["CODE_BRANCH"]:
    kustomization_path = "kustomize/overlays/prod/kustomization.yaml"
  else: 
    kustomization_path = "kustomize/overlays/"+os.environ["CODE_BRANCH"]+"/kustomization.yaml"
  user_dockerhub = os.environ["DOCKER_IMAGE"].split("/")[0]
  repo_name_dockerhub = os.environ["DOCKER_IMAGE"].split(":")[0].split("/")[1]
  image_tag = os.environ["DOCKER_IMAGE"].split(":")[1]
  if "backend" or "be" in os.environ["CODE_REPO_NAME"]:
    tier = "backend"
  elif "frontend" or "fe" in os.environ["CODE_REPO_NAME"]:
    tier = "frontend"
  else:
    raise Exception("code repo tier not recognize")
  
  for filename in os.listdir("kustomize/base/"):
        with open(os.path.join("kustomize/base/", filename)) as file:
            input = yaml.load(file, Loader=yaml.FullLoader)
        if input["kind"] == "Deployment":
            if input["spec"]["template"]["metadata"]["labels"]["tier"] == tier:
                imageName = input["spec"]["template"]["spec"]["containers"][0]["name"]
                break

  with open(kustomization_path) as file:
    kustomization = yaml.load(file, Loader=yaml.FullLoader)
  
  entry = {"name" : imageName, "newName" : user_dockerhub+"/"+repo_name_dockerhub, "newTag" : image_tag}

  if "images" not in kustomization.keys():
    kustomization["images"] = [entry]
    #aggiungo scrivendo, la key patch
    with open(kustomization_path, "w") as file:
        yaml.dump(kustomization, file)
  else:
    #vuol dire che la entry patch esiste, ma non è detto che esista nella sua lista, il list_value necessario
    found = False #inizializzo la variabile
    for e in kustomization["images"]:
        if e["name"] == imageName:
          found = True
          kustomization["patches"].remove(e)
          kustomization["patches"].append(entry)
          break
    if found == False:
        kustomization["patches"].append(entry)
    with open(kustomization_path, "w") as file:
        yaml.dump(kustomization, file)
  

      
if __name__ == '__main__':
    main()
