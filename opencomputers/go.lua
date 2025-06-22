env = {}
require("elsa")

function tryrequire(...)
    return pcall(require, ...)
end

loadfile("apis/computer.lua")(env)
loadfile("apis/os.lua")(env)
loadfile("apis/system.lua")(env)
loadfile("apis/unicode.lua")(env)
loadfile("apis/userdata.lua")(env)
loadfile("apis/uuid.lua")(env)
loadfile("apis/component.lua")(env)


local function runtestthing()
    dofile("_bios/machine.lua")
    print(package.path)
end

co = coroutine.create(runtestthing)
-- coroutine.resume(co)
