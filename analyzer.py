import sys, os, re, ast
from multiprocessing import Pool
import graph

DIRECTORY_PATH:str
FILE_PATH_LIST = set()

def main():
    global DIRECTORY_PATH
    try:
        DIRECTORY_PATH = sys.argv[1]
    except:
        print("Argument error")
        exit()
    if os.path.isdir(DIRECTORY_PATH):
        filepath = find_files_by_ext(DIRECTORY_PATH, "py")
        inp = mproc_file_analyzar(filepath)
        graph.main(inp)
    else:
        print("directory error\nno such directory")



def find_files_by_ext(dir:str, extension:str) -> list:
    global FILE_PATH_LIST
    counter = 0
    match_files = []
    for curDir, _, files in os.walk(dir):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext == "." + extension:
                counter += 1
                file_path = os.path.join(curDir,file)
                match_files.append(file_path)
                FILE_PATH_LIST.add(file_path)
    print("total file:{}".format(counter))
    return match_files



def mproc_file_analyzar(filepath:list):
    mproc = Pool()
    output = mproc.map(file_analyzar, filepath)
    mproc.close()
    return output
    



def file_analyzar(filepath:str) -> list: # [filename, [def], [imp]]
    with open(filepath) as f:
        fdata:str = f.read()
        imp = extract_imp(fdata, filepath)
        return [filepath, imp]



def extract_imp(fdata:str, filepath) -> list: # [[file1, [import1, import2]], [file2, [import1]]...]
    global DIRECTORY_PATH
    global FILE_PATH_LIST
    ret = []
    tree = ast.parse(fdata)

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imp = alias.name.replace(".", "/")
                dir = os.path.dirname(filepath)
                if(os.path.isfile(dir + "/" + imp + ".py")):
                    ret.append([dir + "/" +  imp + ".py", []])
                elif(os.path.isdir(dir + "/" + imp)):
                    ret.append([dir + "/" + imp, []])
                elif(os.path.isfile(imp + ".py")):
                    ret.append([imp + ".py", []])
                elif(os.path.isdir(imp)):
                    ret.append([imp, []])
                else:
                    m = re.findall(r'(.*/).*', dir)
                    flag = True
                    while len(m) != 0:
                        dir = str(m[0])[:-1]
                        if (os.path.isfile(dir + "/" + imp + ".py")):
                            ret.append([dir + "/" + imp + ".py", []])
                            flag = False
                            break
                        elif(os.path.isdir(dir + "/" + imp)):
                            ret.append([dir + "/" + imp, []])
                            flag = False
                            break
                        m = re.findall(r'(.*/).*', dir)
                    if flag:
                        ret.append([alias.name, []])
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                if module is not None:
                    imp = module.replace(".", "/")
                else:
                    imp = ""
                dir = os.path.dirname(filepath)
                if(os.path.isfile(dir + "/" + imp + ".py")):
                    ret.append([dir + "/" + imp + ".py", [alias.name]])
                elif(os.path.isdir(dir + "/" + imp)):
                    ret.append([dir + "/" + imp, [alias.name]])
                elif(os.path.isfile(imp + ".py")):
                    ret.append([imp + ".py", [alias.name]])
                elif(os.path.isdir(imp)):
                    ret.append([imp, [alias.name]])
                else:
                    m = re.findall(r'(.*/).*', dir)
                    flag = True
                    while len(m) != 0:
                        dir = str(m[0])[:-1]
                        if (os.path.isfile(dir + "/" + imp + ".py")):
                            ret.append([dir + "/" + imp + ".py", [alias.name]])
                            flag = False
                            break
                        elif(os.path.isdir(dir + "/" + imp)):
                            ret.append([dir + "/" + imp, [alias.name]])
                            flag = False
                            break
                        m = re.findall(r'(.*/).*', dir)
                    if flag:
                        ret.append([alias.name, [alias.name]])
    return ret



if __name__ == "__main__":
    main()
