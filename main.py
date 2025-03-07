from dataclasses import dataclass
import json
import random
from flask import Flask, request, send_file, redirect, abort, make_response
from flask_swagger_ui import get_swaggerui_blueprint

from blocks import BLOCKS, get_block
from world import World

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    "/docs",
    "/docs/api.yml",
)

@app.route("/docs/api.yml", methods=["GET"])
def apiyml(): return send_file("api.yml")

app.register_blueprint(swaggerui_blueprint)

@dataclass
class Session:
    world: World
    name: str
    play_id: int
    camx: int
    camy: int

    def to_dict(self):
        return { "seed": self.world.seed, "changes": len(self.world.changed), "name": self.name, "pid": self.play_id, "coords": { "x": self.camx, "y": self.camy } }

sessions = dict() # type: dict[int, Session]

@app.route("/", methods=["GET"])
def home():
    return redirect("/docs")

@app.route("/play", methods=["GET"])
def play():
    seed = request.args.get("seed")
    if not seed:
        seed = random.randint(1, int(1e10))
    play_id = random.randint(1, int(1e10))
    world = World(int(seed))
    sessions[play_id] = Session(world, request.args.get("name"), play_id, 0, world.default_height_at(0))
    return { "play_id": play_id }

@app.route("/debug", methods=["GET"])
def debug():
    return [ sessions[s].to_dict() for s in sessions ]


def get_session():
    pid = request.args.get("pid")
    if pid is None:
        return abort(401)
    try:
        pid = int(pid)
    except:
        return abort(400)
    for s in sessions:
        if s == pid:
            return sessions[s]
    return abort(401)

VIEW_WIDTH = 16
VIEW_HEIGHT = 16
@app.route("/view", methods=["GET"])
def view():
    session = get_session()
    if session is None:
        return abort(401)
    out = [] # type: list[list[int | None]]
    for vh in range(VIEW_HEIGHT):
        cur = []
        for vw in range(VIEW_WIDTH):
            block = session.world.get_block_at(session.camx + vw, session.camy + vh)
            cur.append(block.id if block is not None else None)
        out.append(cur)
    return { "world": out if "string" not in request.args else [ ".".join([ (str(n) if n is not None else " ") for n in ns ]) for ns in out ], "camera": { "width": VIEW_WIDTH, "height": VIEW_HEIGHT, "x": session.camx, "y": session.camy } }

@app.route("/blocks", methods=["GET"])
def blocks():
    bl = []
    for b in BLOCKS:
        bl.append({ "block_id": b.id, "name": b.name })
    return bl

@app.route("/move", methods=["POST"])
def move():
    session = get_session()
    data = request.json
    dx, dy = data["dx"], data["dy"]
    session.camx += dx
    session.camy += dy
    r = make_response()
    r.status_code = 204
    return r

@app.route("/place", methods=["PUT"])
def place():
    session = get_session()
    data = request.json
    bid, x, y = int(data["block_id"]), int(data["x"]), int(data["y"])
    session.world.set_block_at(x, y, get_block(bid))
    r = make_response()
    r.status_code = 204
    return r

@app.route("/break", methods=["DELETE"])
def break_():
    session = get_session()
    x, y = int(request.args.get("x")), int(request.args.get("y"))
    session.world.set_block_at(x, y, None)
    r = make_response()
    r.status_code = 204
    return r

@app.route("/save", methods=["GET"])
def save():
    session = get_session()
    c = session.world.changed
    sessions.pop(session.play_id)
    return {
        "changes": [ { "x": coords[0], "y": coords[1], "block_id": c[coords].id if c[coords] is not None else None } for coords in c ],
        "meta": {
            "seed": session.world.seed,
            "name": session.name,
        }
    }



if __name__ == "__main__":
    app.run()

