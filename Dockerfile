FROM ghcr.io/astral-sh/uv:python3.13-bookworm as base

WORKDIR /
ADD pyproject.toml uv.lock /
RUN uv sync --no-default-groups

# ===== #

FROM base as api

ENV PORT=8000
EXPOSE 8000

RUN uv sync --no-default-groups --group flask
ADD alembic.ini /
ADD migrations migrations
ADD main.py /
ADD --chmod=0755 start_scripts/flask.sh start.sh

ENTRYPOINT [ "/start.sh" ]

# ===== #

FROM base as socket
EXPOSE 9999

RUN uv sync --no-default-groups --group socket
ADD --chmod=0755 start_scripts/socket.py start.py
ENTRYPOINT [ "/start.py" ]

# ===== #

FROM nickblah/lua:5.3-luarocks AS oc

RUN apt-get update -y
RUN apt-get install -y subversion build-essential libssl-dev libsdl2-dev
RUN luarocks install luafilesystem
RUN luarocks install luautf8
RUN luarocks install luasocket
RUN luarocks install luasec

ADD https://github.com/zenith391/OCEmu.git /OCEmu
RUN cd OCEmu/luaffifb && luarocks make

ADD https://github.com/GTNewHorizons/OpenComputers.git#:src/main/resources/assets/opencomputers/lua /OCEmu/src/lua
ADD https://github.com/GTNewHorizons/OpenComputers.git#:src/main/resources/assets/opencomputers/loot /OCEmu/src/loot
ADD https://raw.githubusercontent.com/GTNewHorizons/OpenComputers/refs/heads/master/src/main/resources/assets/opencomputers/font.hex /OCEmu/src

# fix an old patch from OCEmu
RUN sed -i -e 's/nreqt.create = nil/nreqt.create = socket.tcp/' /OCEmu/src/support/http_patch.lua

ARG oc_dir="tests/test_opencomputers"

ADD ${oc_dir}/entrypoint.lua ${oc_dir}/setup.lua /OCEmu/src/
ADD ${oc_dir}/ocemu.cfg /root/.ocemu/
ADD ${oc_dir}/init.lua ${oc_dir}/autorun.lua /OCEmu/src/loot/openos/

WORKDIR /OCEmu/src/
ENTRYPOINT [ "/usr/local/bin/lua" ]
CMD ["entrypoint.lua"]