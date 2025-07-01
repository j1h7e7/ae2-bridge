local c = require("bridge.socket_handler")
local M = {}

M.message_types = {
    item_count = "item_count"
}

function M.init()
    local client = {}

    client.con = c.create_connection("http://127.0.0.1", 9999)

    function client._send(message_type, data)
        data['event_type'] = message_type
        client.con.send(data)
        return client.con.read()
    end

    function client.item_count(item_name, item_count)
        return client._send("item_count", { item_name = item_name, item_count = item_count })
    end

    return client
end

return M
