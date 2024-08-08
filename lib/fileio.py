import os
import copy
to_import = {"debug":"dbg"}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

def get_formula(filename):
    file = open('lib/data/'+filename)
    content = file.read()
    content = content.replace('\n', '')
    content = content.replace('\r', '')
    content = content.replace('\t', '')
    output = eval(content)
    return copy.deepcopy(output)
def get_effect_map_instruction(filename):
    file = open('lib/data/'+filename)
    content = file.read()
    raise dbg.UnimplementError()
