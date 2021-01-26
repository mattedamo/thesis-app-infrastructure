import shutil, os
#you cannot delete prod directory since you cannot delete master branch in code repos
def main():
      branch = os.environ["CODE_BRANCH"]
      tier = os.environ["TIER"]
      list_branch = branch.split("/")
      if(len(list_branch) == 2 and (list_branch[0] == "features" or list_branch[0] == "releases")):
        endPath = tier+"/"+branch
      else:
        raise Exception("not existing branch")
      
      shutil.rmtree("kustomize/overlays/"+endPath, ignore_errors=True)

if __name__ == '__main__':
    main()
