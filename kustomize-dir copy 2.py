import shutil, os

def main():
  #print(os.listdir("./kustomize/kustomize/overlays/dev/"))   
  shutil.rmtree("./kustomize/kustomize/overlays/dev/")
  #print(os.listdir("./kustomize/kustomize/overlays/dev/"))   

if __name__ == '__main__':
    main()
