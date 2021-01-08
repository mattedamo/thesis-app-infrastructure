import yaml, os
#from yaml_update import yaml_updates
#from kind_name import getKindName

def getKindName(tierValue):
    tierValue = tierValue
    kind_name = {}
    for filename in os.listdir("kustomize/base/"):
        with open(os.path.join("kustomize/base/", filename)) as file:
            input = yaml.load(file, Loader=yaml.FullLoader)
        if input["kind"] == "Deployment":
            if input["spec"]["template"]["metadata"]["labels"]["tier"] == tierValue:
                kind_name["deployment"] = input["metadata"]["name"]
        elif input["kind"] == "Service":
            if input["spec"]["selector"]["tier"] == tierValue:
                kind_name["service"] = input["metadata"]["name"]
    return kind_name

def yaml_updates(be, ns_path, kind_name, tier):
    tier = tier
    for x in be:
        if(x["type"] == "deployment"):
            x.pop("type")
            update_deployment(x, kind_name["deployment"], ns_path, tier)



def update_deployment(values, kind_name, ns_path, tier):
    print(values, kind_name, ns_path, tier)
    for k,v  in values.items():
        if(k == "replicas"):
            patch_deployment(ns_path, k, v, kind_name, tier)

def patch_deployment(ns_path, key, value, kind_name, tier):
    print(ns_path)
    kustomize_path = ns_path + "kustomization.yaml"
    with open(kustomize_path) as file:
            kustomization = yaml.load(file, Loader=yaml.FullLoader)
    
    if "patches" not in kustomization.keys():
        entry = [{"target": {"name" : kind_name, "labelSelector" : "tier="+tier}, "path" : tier+"_"+kind_name+"_patch.yaml"}]
        kustomization["patches"] = entry
        with open(kustomize_path, "w") as file:
            yaml.dump(kustomization, file)
    else:
        found = False
        for entry in kustomization["patches"]:
            if entry["path"] == tier+"_"+kind_name+"_patch.yaml":
                found = True
            if found == False:
                entry = [{"target": {"name" : kind_name, "labelSelector" : "tier="+tier}, "path" : tier+"_"+kind_name+"_patch.yaml"}]
                kustomization["patches"] = entry
                with open(kustomize_path, "w") as file:
                    yaml.dump(kustomization, file)
    
    #adesso devo aggiungere il file patch.yaml
    found = False
    for filename in os.listdir(ns_path):
        if filename == tier+"_"+kind_name+"_patch.yaml":
            found = True
    if(found == False):
        #with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "x") as file:
        #    patch = yaml.load(file, Loader=yaml.FullLoader)
        open(ns_path+tier+"_"+kind_name+"_patch.yaml", "x")
        patch = []
    else:
        with open(ns_path+tier+"_"+kind_name+"_patch.yaml") as file:
            patch = yaml.load(file, Loader=yaml.FullLoader)

    if(key == "replicas"):
        if(patch != None):
            for ele in patch:
                found = False
                if(ele["path"] == "/spec/replicas"):
                    ele["value"] = value
                    found = True
            if(found == False):
                patch.append(dict({"op" : "add", "path" : "/spec/replicas", "value" : 33}))
            with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "w") as file:
                yaml.dump(patch, file)
        else:
            patch = [{"op" : "add", "path" : "/spec/replicas", "value" : 33}]
            with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "w") as file:
                yaml.dump(patch, file)
    

def update_service(values, kind_name, ns_path, tier):
    for k,v  in values.items():
        if(k == "port"):
            patch_service(ns_path, k, v, kind_name, tier)

def patch_service(ns_path, key, value, kind_name, tier):
    kustomize_path = ns_path + "kustomization.yaml"
    with open(kustomize_path) as file:
            kustomization = yaml.load(file, Loader=yaml.FullLoader)
    
    if "patches" not in kustomization.keys():
        entry = [{"target": {"name" : kind_name, "labelSelector" : "tier="+tier}, "path" : tier+"_"+kind_name+"_patch.yaml"}]
        kustomization["patches"] = entry
        with open(kustomize_path, "w") as file:
            yaml.dump(kustomization, file)
    else:
        found = False
        for entry in kustomization["patches"]:
            if entry["path"] == tier+"_"+kind_name+"_patch.yaml":
                found = True
            if found == False:
                entry = [{"target": {"name" : kind_name, "labelSelector" : "tier="+tier}, "path" : tier+"_"+kind_name+"_patch.yaml"}]
                kustomization["patches"] = entry
                with open(kustomize_path, "w") as file:
                    yaml.dump(kustomization, file)
    
    #adesso devo aggiungere il file patch.yaml
    found = False
    for filename in os.listdir(ns_path):
        if filename == tier+"_"+kind_name+"_patch.yaml":
            found = True
    if(found == False):
        with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "x") as file:
            patch = yaml.load(file, Loader=yaml.FullLoader)
    else:
        
        with open(ns_path+tier+"_"+kind_name+"_patch.yaml") as file:
            patch = yaml.load(file, Loader=yaml.FullLoader)

    if(key == "replicas"):
        if(patch != None):
            for ele in patch:
                found = False
                if(ele["path"] == "/spec/replicas"):
                    ele["value"] = value
                    found = True
            if(found == False):
                patch.append(dict({"op" : "add", "path" : "/spec/replicas", "value" : 33}))
            with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "w") as file:
                yaml.dump(patch, file)
        else:
            patch = [{"op" : "add", "path" : "/spec/replicas", "value" : 33}]
            with open(ns_path+tier+"_"+kind_name+"_patch.yaml", "w") as file:
                yaml.dump(patch, file)

def main():
  
    with open("./file.yaml") as file:
        input = yaml.load(file, Loader=yaml.FullLoader)
    #prima controllo quale è il namespace e lo rimuovo siccome non mi serve più

    if "ns" not in input:
        raise Exception("missing ns")
    else:
        ns_path = "kustomize/overlays/"+input['ns']+"/"
        input.pop('ns')

    be = None
    fe = None
    db = None

    for k,v in input.items():
        if k == "backend":
            be = v
        elif k == "frontend":
            fe = v
        elif k == "db":
            db = v
    
    if be != None:
        kind_name = getKindName("backend")
        yaml_updates(be, ns_path, kind_name, "backend")

if __name__ == '__main__':
    main()
