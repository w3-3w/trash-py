import json

s = '[{"requesttype":"userinfo","user":"1","info":"hello!!"}]'
jsonfile = json.JSONDecoder().decode(s)
print(jsonfile[0]["requesttype"])
print(type(s))
print(type(jsonfile[0]))
