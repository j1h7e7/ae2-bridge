FROM nickblah/lua:5.3-luarocks AS oc

RUN apt-get update -y
RUN apt-get install -y subversion build-essential libssl-dev libsdl2-dev
RUN luarocks install luafilesystem
RUN luarocks install luautf8
RUN luarocks install luasocket
RUN luarocks install luasec

ADD https://github.com/zenith391/OCEmu.git /OCEmu
RUN cd OCEmu/luaffifb && luarocks make

ADD https://github.com/MightyPirates/OpenComputers.git#:src/main/resources/assets/opencomputers/lua /OCEmu/src/lua
ADD https://github.com/MightyPirates/OpenComputers.git#:src/main/resources/assets/opencomputers/loot /OCEmu/src/loot
ADD https://raw.githubusercontent.com/MightyPirates/OpenComputers/refs/heads/master-MC1.7.10/src/main/resources/assets/opencomputers/font.hex /OCEmu/src

# fix an old patch from OCEmu
RUN sed -i -e 's/nreqt.create = nil/nreqt.create = socket.tcp/' /OCEmu/src/support/http_patch.lua

ADD ./boot2.lua ./main2.lua ./test.lua /OCEmu/src/
ADD ./ocemu.cfg /root/.ocemu/
ADD ./init.lua ./autorun.lua /OCEmu/src/loot/openos/

WORKDIR /OCEmu/src/
ENTRYPOINT [ "/bin/sh" ]