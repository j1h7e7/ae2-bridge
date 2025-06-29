local mai = {}
local obj = {}
-- TODO: is this info correct?
local di = {
    class = "generic",
    description = "AE2 Bridge",
    vendor = "MightyPirates GmbH & Co. KG",
    product = ""
}


local function _make_item(name, size)
    return {
        name = name,
        damage = 0,
        maxDamage = 0,
        size = size,
        maxSize = 64,
        label = "",
        hasTag = false,
        tag = nil,
        crop = nil,
        inputs = nil,
        outputs = nil,
    }
end

mai.allItems = { doc = "function():userdata -- Get an iterator object for the list of the items in the network." }
function obj.allItems()
    local item1 = _make_item("me_item", 1)
    local item2 = _make_item("me_item", 2)
    local items = { item1, item2 }

    local i = 0
    return function()
        i = i + 1
        if i <= #items then return items[i] end
    end
end

return obj, nil, mai, di
