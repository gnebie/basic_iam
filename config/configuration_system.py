from json import JSONEncoder


# json encode
old_default = JSONEncoder.default

def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, TextClause):
        return str(obj)
    if isinstance(obj, User):
        return old_default(self,user_to_dto(obj))
    return old_default(self, obj)

JSONEncoder.default = new_default
