#!/usr/bin/lua5.2
if package.cpath:find(".dll", nil, true) then
    package.cpath = ".\\extras\\?.dll;" .. package.cpath
    package.path = ".\\extras\\?\\init.lua;.\\extras\\?.lua;" .. package.path
end

local ffi = require("ffi")
local SDL = require("sdl2.init")
local lfs = require("lfs")
local arg_parse = require("support.arg_parse")
local socket = require("socket")

local args, options = arg_parse(...)
local baseDir = os.getenv("HOME") .. "/.ocemu"

function boot()
    local wen = {}
    for k, v in pairs(SDL) do
        if k:sub(1, 12) == "WINDOWEVENT_" then
            wen[v] = k:sub(13):lower()
        end
    end

    local recursiveDelete
    function recursiveDelete(path)
        local mode = lfs.attributes(path, "mode")
        if mode == nil then
            return false
        elseif mode == "directory" then
            local stat = true
            for entry in lfs.dir(path) do
                if entry ~= "." and entry ~= ".." then
                    local mode = lfs.attributes(path .. "/" .. entry, "mode")
                    if mode == "directory" then
                        recursiveDelete(path .. "/" .. entry)
                    end
                    os.remove(path .. "/" .. entry)
                end
            end
        end
        return os.remove(path)
    end

    elsa = {
        args = args,
        opts = options,
        getError = function() return ffi.string(SDL.getError()) end,
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
                return ffi.os
            end,
        },
        handlers = {},
        SDL = SDL,
        windowEventID = wen,
    }
    local handlers = elsa.handlers

    setmetatable(elsa, {
        __index = function(t, k)
            return function(...)
                if handlers[k] ~= nil then
                    local hndtbl = handlers[k]
                    for i = 1, #hndtbl do
                        hndtbl[i](...)
                    end
                end
            end
        end,
        __newindex = function(t, k, v)
            if handlers[k] == nil then
                handlers[k] = {}
            end
            local hndtbl = handlers[k]
            hndtbl[#hndtbl + 1] = v
        end
    })

    math.randomseed(0)
    require("setup")
end

boot()
co = boot_machine()

repeat
    running = coroutine.resume(co)
    socket.sleep(0.2)
until not running
