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

function M.CreateConnection(host, port)
    local con = {}

    con.soc = i.open(host, port)

    function con.send(data)
        con.soc:write(json_dump(data) .. "\n")
    end

    return con
end

return M
