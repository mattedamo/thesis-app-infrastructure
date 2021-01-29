import yaml, os, shutil
def create_basic_struct():
  os.makedirs("kustomize/overlays/backend", exist_ok=True)
  os.makedirs("kustomize/overlays/frontend", exist_ok=True)

def create_specific_struct(val, path, folder):
  if val in os.listdir(path):
      #delete path
      shutil.rmtree(folder, ignore_errors=True)
  #create path
  os.makedirs(folder, exist_ok= True)
    
def create_kustomization(branch, list_branch, folder, tier, app_name):
  k = {}
  k["kind"] = "Kustomization"
  k["apiVersion"] = "kustomize.config.k8s.io/v1beta1"
  if branch == "master":
    k["resources"] = ["../../base"]
    k["namespace"] = app_name+"-prod"
    open(folder+"/kustomization.yaml", "x")

    with open(folder+"/kustomization.yaml", "w") as file:
        yaml.dump(k, file)
  else: 
    k["resources"] = ["../../../../base"]
    k["namespace"] = app_name+"-"+tier+"-"+list_branch[0]+"-"+list_branch[1]
    open(folder+list_branch[-1]+"/kustomization.yaml", "x")

    with open(folder+list_branch[-1]+"/kustomization.yaml", "w") as file:
          yaml.dump(k, file)

def main():
  branch = os.environ["CODE_BRANCH"]
  tier = os.environ["TIER"]
  app_name = os.environ["APP_NAME"]
  list_branch = branch.split("/")
  
  create_basic_struct()

  if(len(list_branch) == 1 and branch == "master"):
    folder = "kustomize/overlays/prod/"
    create_specific_struct("prod", "kustomize/overlays", folder)
  else:
    overlays = "kustomize/overlays/"+tier+"/"
    if(len(list_branch) == 2 and "features" == list_branch[0] and len(list_branch[1].strip())>0):
      folder = overlays+"features/"
      create_specific_struct("features", overlays, folder)
    elif(len(list_branch) == 2 and "releases" == list_branch[0] and len(list_branch[1].strip())>0):
      folder = overlays+ "releases/"
      create_specific_struct("releases", overlays, folder)
    else:
      raise Exception("Branch is not correct!")

  #create kustomization.yaml
  create_kustomization(branch, list_branch, folder, tier, app_name)


if __name__ == '__main__':
    main()
