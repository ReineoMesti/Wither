import copy

to_import = {"display":"disp", "expandrandom":"exrand",
             "debug":"dbg", 'fileio':'fio'}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

