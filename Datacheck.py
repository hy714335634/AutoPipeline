def isexists(obj,key):
    if obj and key in obj.keys():
        return obj[key]
    else:
        return ""