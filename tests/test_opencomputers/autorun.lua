local c = require("bridge/socketHandler")

local con = c.CreateConnection("http://127.0.0.1", 9999)

con.send({ item_count = 5, item_name = "lua_item", event_type = "item_count" })
con.soc:read()
