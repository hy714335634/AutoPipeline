def isexists(obj,key,**kwags):
    if obj and key in obj.keys():
        return obj[key]
    else:
        if "default" in kwags.keys():
            return kwags["default"]
        else:
            return ""