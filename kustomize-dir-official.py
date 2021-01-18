import yaml, os
def create_kustomization(branch, list_branch, folder, tier):
  k = {}
  k["kind"] = "Kustomization"
  k["apiVersion"] = "kustomize.config.k8s.io/v1beta1"
  if branch == "master":
    k["resources"] = ["../../base"]
    k["namespace"] = "thesis-app-prod"

    with open(folder+"/kustomization.yaml", "w") as file:
        yaml.dump(k, file)
  else: 
    k["resources"] = ["../../../../base"]
    k["namespace"] = "thesis-app-"+tier+"-"+list_branch[0]+"-"+list_branch[1]
    with open(folder+list_branch[-1]+"/kustomization.yaml", "w") as file:
          yaml.dump(k, file)

def main():
  branch = os.environ["CODE_BRANCH"]
  tier = os.environ["TIER"]
  list_branch = branch.split("/")
  if(len(list_branch) == 1 and branch == "master"):
    folder = "kustomize/overlays/prod"
    if "prod" not in os.listdir("kustomize/overlays"):
      #create path
      os.mkdir(folder)
      #create kustomization.yaml
      create_kustomization(branch, list_branch, folder, tier)
    else:
      if("kustomization.yaml" not in os.listdir(folder)):
        #create kustomization.yaml
        create_kustomization(branch, list_branch, folder, tier)
  else:
    overlays = "kustomize/overlays/"+tier+"/"
    if(len(list_branch) == 2 and "features" == list_branch[0] and len(list_branch[1].strip())>0):
      folder = overlays+"features/"
      if "features" not in os.listdir(overlays):
        #create path
        os.makedirs(overlays+branch)
      elif list_branch[1] not in os.listdir(folder):
        #create path
        os.mkdir(folder+list_branch[1])
        
    elif(len(list_branch) == 2 and "releases" == list_branch[0]and len(list_branch[1].strip())>0):
      folder = overlays+ "releases/"
      if "releases" not in os.listdir(overlays):
        #create path
        os.makedirs(overlays+branch)
      elif list_branch[0] not in os.listdir(folder):
        #create path
        os.mkdir(folder+list_branch[0])
    else:
      raise Exception("Branch name is not correct!")

    if("kustomization.yaml" not in os.listdir(folder+list_branch[1])):
        #create kustomization.yaml
        create_kustomization(branch, list_branch, folder, tier)

      
if __name__ == '__main__':
    main()
