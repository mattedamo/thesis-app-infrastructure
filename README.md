### kustomize dir structuree
```
kustomize/ -> /base/ #basic yaml files
              /overlays ->  /prod
                            /frontend -> /features -> /name1/
                                                      /nameN/
                                         /releases -> /name1/
                                                      /nameN/
                            /backend  -> /features/...
                                      -> /releases/...

``` 
