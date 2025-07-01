local component = require("component")
local client = require("bridge.client")

local controller = component.me_controller
local cl = client.init()

for itemstack in controller.allItems() do
    cl.item_count(itemstack.name, itemstack.size)
end
