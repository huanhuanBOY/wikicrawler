import os
import json
class dirStructure:
    def files_folder(self, path):
        files = []
        folders = []
        for d in os.listdir(path):
            if os.path.isdir(path+"/"+d):
                print(d)
                folders.append(d)
            else:
                files.append(d)
        return files, folders
    
    def runDir(self, prefixed, name):
        localpath = prefixed + "/" +name
        f, d = self.files_folder(localpath)
        tmp = {"page":f, "cate":{}}
        for i in d:
            print(i)
            tmp["cate"][i] = self.runDir(localpath, i)
        return tmp
    
    def runKey(self, prefixed, name):
        localpath = prefixed + "/" +name
        f, d = self.files_folder(localpath)
        others = []
        for i in f:
            if i.replace(".txt","").replace("_","").strip() != "":
                others.append( i.replace(".txt","") )
        children = {"others": others}
        for i in d:
            if i.replace(".txt","").replace("_","").strip() != "":
                children[i.replace(".txt","")] = self.runKey(localpath, i)
        return children

data = (dirStructure()).runKey(".","CalculusKey")
with open("math_structure.json", "w+") as f:
    f.write(json.dumps(data))
# data = (dirStructure()).run(".","Mathematics")
# with open("math_structure.txt", "w+") as f:
#     f.write(json.dumps(data))