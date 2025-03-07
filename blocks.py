from dataclasses import dataclass

@dataclass(order=True)
class Block:
    id: int
    name: str

    def __iter__(self):
        return iter((self.id, self.name))

def get_block(id: int):
    for b in BLOCKS:
        if b.id == id: return b

BLOCKS = [
    Block(1, "Dirt"),
    Block(2, "Grass"),
    Block(3, "Stone"),
    Block(4, "Sand"),
    Block(5, "Log"),
    Block(6, "Leaves"),
    Block(7, "Glass"),
    Block(8, "Planks"),
    Block(9, "Stairs R"),
    Block(10, "Stairs L"),
    Block(11, "Mud"),
    Block(12, "Bricks"),
    Block(13, "Obsidian"),
    Block(14, "Clay"),
    Block(15, "Ice"),
    Block(16, "Wool"),
    Block(17, "Sandstone"),
    Block(18, "Cobblestone"),
    Block(19, "Concrete"),
]

DIRT = BLOCKS[0]
GRASS = BLOCKS[1]
STONE = BLOCKS[2]
SAND = BLOCKS[3]
LOG = BLOCKS[4]
LEAVES = BLOCKS[5]
COBBLESTONE = BLOCKS[17]
