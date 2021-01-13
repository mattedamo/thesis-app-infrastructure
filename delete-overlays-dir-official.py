import shutil, os

def main():
      branch = os.environ["CODE_BRANCH"]
      list_branch = branch.split("/")
      if(len(list_branch) == 1 and branch=="master"):
        endPath = "prod/"
      elif(len(list_branch) == 2 and (list_branch[0] == "features" or list_branch[0] == "releases")):
        endPath = branch
      else:
        raise Exception("not existing branch")
      
      shutil.rmtree("kustomize/overlays/"+endPath)

if __name__ == '__main__':
    main()
