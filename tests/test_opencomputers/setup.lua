function math.trunc(n)
    return n < 0 and math.ceil(n) or math.floor(n)
end

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

function tryrequire(...)
    return pcall(require, ...)
end

function string_trim(s)
    local from = s:match "^%s*()"
    return from > #s and "" or s:match(".*%S", from)
end

-- load configuration
elsa.filesystem.load("config.lua")()
config.load()
elsa.filesystem.load("settings.lua")()

function elsa.quit()
    config.save()
end

local maxCallBudget = (1.5 + 1.5 + 1.5) / 3 -- T3 CPU and 2 T3+ memory

machine = {
    starttime = elsa.timer.getTime(),
    deadline = elsa.timer.getTime(),
    signals = {},
    totalMemory = 2 * 1024 * 1024,
    insynccall = false,
    callBudget = maxCallBudget,
}

function machine.consumeCallBudget(callCost) return true end

function machine.beep(frequency, duration) end

cprint = function(...) end

if not machine.sleep then
    local sok, socket = tryrequire("socket")
    if sok then
        function machine.sleep(s)
            socket.sleep(s)
        end
    end
end
if not machine.sleep then
    function machine.sleep() end
end


local env = {
    _VERSION = "Lua 5.3",
    assert = assert,
    collectgarbage = collectgarbage,
    coroutine = coroutine,
    debug = debug,
    error = error,
    getmetatable = getmetatable,
    io = io,
    ipairs = ipairs,
    load = load,
    math = math,
    next = next,
    pairs = pairs,
    pcall = pcall,
    print = print,
    rawequal = rawequal,
    rawget = rawget,
    rawlen = rawlen,
    rawset = rawset,
    require = require,
    select = select,
    setmetatable = setmetatable,
    string = string,
    table = table,
    tonumber = tonumber,
    tostring = tostring,
    type = type,
    utf8 = utf8,
    xpcall = xpcall,
}

setmetatable(env, {
    __index = function(_, k)
        cprint("Missing environment access", "env." .. k)
    end,
})

-- load api's into environment
elsa.filesystem.load("apis/computer.lua")(env)
elsa.filesystem.load("apis/os.lua")(env)
elsa.filesystem.load("apis/system.lua")(env)
elsa.filesystem.load("apis/unicode.lua")(env)
elsa.filesystem.load("apis/userdata.lua")(env)
elsa.filesystem.load("apis/uuid.lua")(env)
elsa.filesystem.load("apis/component.lua")(env)

function boot_machine()
    -- load machine.lua
    local machine_data, err = elsa.filesystem.read("lua/machine.lua")
    if machine_data == nil then
        error("Failed to load machine.lua:\n\t" .. tostring(err))
    end
    local machine_fn, err = load(machine_data, "=machine", "t", env)
    if machine_fn == nil then
        error("Failed to parse machine.lua\n\t" .. tostring(err))
    end
    return coroutine.create(machine_fn)
end
