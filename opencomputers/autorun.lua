local i = require("internet")

con = i.open("http://127.0.0.1", 9999)

con:write('{"item_count":5,"item_name":"lua_item","event_type":"item_count"}\n')
con:read()
