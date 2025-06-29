local i = require("internet")
local M = {}

local function json_dump(data)
    local parts = {}
    for k, v in pairs(data) do
        local ks = '"' .. k .. '"'
        local vs
        if type(v) == 'number' then
            vs = v
        else
            vs = '"' .. v .. '"'
        end
        table.insert(parts, ks .. ":" .. vs)
    end
    return "{" .. table.concat(parts, ",") .. "}"
end

function M.create_connection(host, port)
    local con = {}

    con.soc = i.open(host, port)
    con.soc:setTimeout(0.1)

    function con.send(data)
        con.soc:write(json_dump(data) .. "\n")
    end

    function con.read()
        return con.soc:read()
    end

    return con
end

return M
