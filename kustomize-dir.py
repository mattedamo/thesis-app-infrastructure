import yaml, os
def create_kustomization(branch, list_branch, folder):
  k = {}
  k["Kind"] = "Kustomization"
  k["Namespace"] = "thesis-app-"+branch
  k["apiVersion"] = "kustomize.config.k8s.io/v1beta1"
  if branch == "master":
    k["resources"] = ["../../base"]
  else: 
    k["resources"] = ["../../../base"]
  with open(folder+list_branch[-1]+"/kustomization.yaml", "w") as file:
        yaml.dump(k, file)

def main():
  branch = os.environ("CODE_BRANCH")
  list_branch = branch.split("/")
  overlays = "thesis-app-infrastructure/kustomize/overlays/"
  if(len(list_branch) == 1 and branch == "master"):
    folder = "kustomize/overlays/prod/"
    if "prod" not in os.listdir(overlays):
      #create path
      os.mkdir(folder)
      #create kustomization.yaml
      create_kustomization(branch, list_branch, folder)
    elif list_branch[0] not in os.listdir(folder):
      #create path
      os.mkdir(folder+list_branch[0])
      #create kustomization.yaml
      create_kustomization(branch, list_branch, folder)
  else:
    if(len(list_branch) == 2 and "features" == list_branch[0]):
      folder = "kustomize/overlays/features/"
      if "features" not in os.listdir(overlays):
        #create path
        os.mkdirs(overlays+branch)
      elif list_branch[0] not in os.listdir(folder):
        #create path
        os.mkdir(folder+list_branch[0])
        
    elif(len(list_branch) == 2 and "releases" == list_branch[0]):
      folder = "kustomize/overlays/releases/"
      if "releases" not in os.listdir(overlays):
        #create path
        os.mkdirs(overlays+branch)
      elif list_branch[0] not in os.listdir(folder):
        #create path
        os.mkdir(folder+list_branch[0])
    else:
      raise Exception("Branch name is not correct!")

    if("kustomization.yaml" not in os.listdir(folder+list_branch[0])):
        #create kustomization.yaml
        create_kustomization(branch, list_branch, folder)

      
if __name__ == '__main__':
    main()
