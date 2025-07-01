local c = require("bridge.client")
local component = require("component")

local client = c.init()

local r1 = client.item_count("lua_item", 1)
local r2 = client.item_count("lua_item", 2)

assert(r1 == "ack", "instead of ack got " .. r1 .. ".")
assert(r2 == "ack", "instead of ack got " .. r2 .. ".")

for item in component.me_interface.allItems() do
    assert(client.item_count(item.name, item.size) == "ack")
end
