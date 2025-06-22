-- local ffi = require("ffi")
-- local SDL = require("sdl2.init")
local lfs = require("lfs")

elsa = {
    args = {},
    opts = {},
    -- getError = function() return ffi.string(SDL.getError()) end,
    filesystem = {
        lines = io.lines,
        load = loadfile,
        read = function(path)
            local file, err = io.open(path, "rb")
            if not file then return nil, err end
            local data = file:read("*a")
            file:close()
            return data, #data
        end,
        write = function(path, data)
            local file, err = io.open(path, "wb")
            if not file then return false, err end
            file:write(data)
            file:close()
            return true
        end,
        exists = function(path)
            return lfs.attributes(path, "mode") ~= nil
        end,
        isDirectory = function(path)
            return lfs.attributes(path, "mode") == "directory"
        end,
        createDirectory = function(path)
            local pstr = ""
            for part in (path .. "/"):gmatch("(.-)[\\/]") do
                pstr = pstr .. part
                lfs.mkdir(pstr)
                pstr = pstr .. "/"
            end
            return lfs.attributes(path, "mode") ~= nil
        end,
        newFile = function(path, mode)
            return io.open(path, mode .. "b")
        end,
        getDirectoryItems = function(path)
            local list = {}
            for entry in lfs.dir(path) do
                if entry ~= "." and entry ~= ".." then
                    list[#list + 1] = entry
                end
            end
            return list
        end,
        getLastModified = function(path)
            return lfs.attributes(path, "modification")
        end,
        getSize = function(path)
            return lfs.attributes(path, "size")
        end,
        getSaveDirectory = function()
            return baseDir
        end,
        remove = function(path)
            return recursiveDelete(path)
        end,
    },
    timer = {
        getTime = function()
            return SDL.getTicks() / 1000
        end,
    },
    system = {
        getOS = function()
            -- return ffi.os
            return 'linux'
        end,
    },
    handlers = {},
    -- SDL = SDL,
    windowEventID = wen,
}

settings = {
    beepSampleRate = 44100,
    beepVolume = 32,
    monochromeColor = tonumber("0xFFFFFF"),

    eepromDataSize = 256,
    eepromSize = 4096,
    allowBytecode = false,
    allowGC = false,
    timeout = 5,

    components = {
        -- { "gpu",        nil, 0,  160,           50,       3 },
        -- { "modem",      nil, 1,  false },
        { "eeprom",     nil, 9,  "lua/bios.lua" },
        { "filesystem", nil, 7,  "loot/openos", "openos", true,  1 },
        { "filesystem", nil, -1, "tmpfs",       "tmpfs",  false, 5 },
        { "filesystem", nil, 5,  nil,           nil,      false, 4 },
        { "internet",   nil, 2 },
        { "computer",   nil, -1 },
        { "ocemu",      nil, -1 },
    },
    emulatorDebug = false,
    fast = true,
    vagueErrors = true,

    floppySize = 512,
    hddPlatterCounts = { 2, 4, 8 },
    hddSizes = { 1024, 2048, 4096 },
    maxReadBuffer = 2048,

    httpEnabled = true,
    tcpEnabled = true,

    maxNetworkPacketSize = 8192,
    maxWirelessRange = 400,
}

local function check(have, want, ...)
    if not want then
        return false
    else
        return have == want or check(have, ...)
    end
end

function checkArg(n, have, ...)
    have = type(have)
    if not check(have, ...) then
        local msg = string.format("bad argument #%d (%s expected, got %s)", n, table.concat({ ... }, " or "), have)
        error(msg, 3)
    end
end

function compCheckArg(n, have, ...)
    have = type(have)
    if not check(have, ...) then
        local msg = string.format("bad arguments #%d (%s expected, got %s)", n, table.concat({ ... }, " or "), have)
        error(msg, 0)
    end
end
