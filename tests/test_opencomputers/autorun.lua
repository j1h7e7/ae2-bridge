local c = require("bridge/socketHandler")

local con = c.CreateConnection("http://127.0.0.1", 9999)

con.send({ item_count = 1, item_name = "lua_item", event_type = "item_count" })
r1 = con.read()
os.sleep(0.4)
con.send({ item_count = 2, item_name = "lua_item", event_type = "item_count" })
r2 = con.read()

assert(r1 == "ack")
assert(r2 == "ack")
