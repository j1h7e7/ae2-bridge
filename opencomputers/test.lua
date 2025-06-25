local socket = require("socket")

dofile("boot2.lua")
co = boot_machine()

repeat
    running = coroutine.resume(co)
    socket.sleep(0.2)
until not running
