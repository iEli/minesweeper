# minesweeper.py

from dataclasses import dataclass
from typing import List, Tuple, Optional, Set
import random
import sys

@dataclass
class Cell:
    is_mine: bool = False
    is_revealed: bool = False
    is_flagged: bool = False
    adj_mines: int = 0

Board = List[List[Cell]]

NEIGHBORS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

class Minesweeper:
    def __init__(self, rows: int = 9, cols: int = 9, mines: int = 10):
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.board: Board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.first_click_done = False
        self.revealed_count = 0
        self.game_over = False
        self.win = False

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int):
        for dr, dc in NEIGHBORS:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                yield nr, nc

    def place_mines(self, safe_rc: Tuple[int,int]):
        sr, sc = safe_rc
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        all_cells.remove((sr, sc))
        mine_positions = set(random.sample(all_cells, self.total_mines))
        for r, c in mine_positions:
            self.board[r][c].is_mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].is_mine:
                    continue
                count = 0
                for nr, nc in self.neighbors(r, c):
                    if self.board[nr][nc].is_mine:
                        count += 1
                self.board[r][c].adj_mines = count

    def reveal(self, r: int, c: int):
        if not self.in_bounds(r, c) or self.board[r][c].is_flagged or self.board[r][c].is_revealed:
            return
        if not self.first_click_done:
            self.place_mines((r, c))
            self.first_click_done = True

        cell = self.board[r][c]
        if cell.is_mine:
            cell.is_revealed = True
            self.game_over = True
            self.win = False
            return

        # flood fill reveal
        stack = [(r, c)]
        visited: Set[Tuple[int,int]] = set()
        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            cur = self.board[cr][cc]
            if cur.is_flagged or cur.is_revealed:
                continue
            cur.is_revealed = True
            self.revealed_count += 1
            if cur.adj_mines == 0:
                for nr, nc in self.neighbors(cr, cc):
                    ncell = self.board[nr][nc]
                    if not ncell.is_revealed and not ncell.is_flagged and not ncell.is_mine:
                        stack.append((nr, nc))

        # check win: all non-mine cells revealed
        non_mine_total = self.rows * self.cols - self.total_mines
        if self.revealed_count == non_mine_total:
            self.game_over = True
            self.win = True

    def toggle_flag(self, r: int, c: int):
        if not self.in_bounds(r, c) or self.board[r][c].is_revealed:
            return
        self.board[r][c].is_flagged = not self.board[r][c].is_flagged

    def render(self) -> str:
        # header
        header = "    " + " ".join(f"{c:2d}" for c in range(self.cols))
        sep = "   " + "-" * (3 * self.cols - 1)
        lines = [header, sep]
        for r in range(self.rows):
            row_str = [f"{r:2d}|"]
            for c in range(self.cols):
                cell = self.board[r][c]
                if self.game_over and cell.is_mine:
                    ch = "*"
                elif cell.is_flagged:
                    ch = "⚑"
                elif not cell.is_revealed:
                    ch = "□"
                else:
                    ch = "·" if cell.adj_mines == 0 else str(cell.adj_mines)
                row_str.append(f" {ch}")
            lines.append(" ".join(row_str))
        # footer with status
        flags = sum(cell.is_flagged for row in self.board for cell in row)
        status = f"Mines: {self.total_mines} | Flags: {flags}\n"
        if self.game_over:
            status += " | " + ("Wow, you somehow won!" if self.win else "You lost... I knew you wouldn't win.")
        lines.append(sep)
        lines.append(status)
        return "\n".join(lines)

def parse_cmd(s: str) -> Optional[Tuple[str, int, int]]:
    parts = s.strip().split()
    if not parts:
        return None
    if parts[0].lower() == "q":
        return ("q", -1, -1)
    if len(parts) != 3 or parts[0].lower() not in ("r", "f"):
        print("Usage: r ROW COL | f ROW COL | q", file=sys.stderr)
        return None
    try:
        cmd = parts[0].lower()
        r = int(parts[1])
        c = int(parts[2])
        return (cmd, r, c)
    except ValueError:
        print("ROW and COL must be integers.", file=sys.stderr)
        return None

def main():
    rows, cols, mines = 9, 9, 10
    if len(sys.argv) in (4,):
        rows, cols, mines = map(int, sys.argv[1:4])
    game = Minesweeper(rows, cols, mines)
    print("\nElias' Minesweeper (better than Google!)")
    print("Commands: r ROW COL, f ROW COL, q")
    print(game.render())

    while not game.game_over:
        cmd_tup = parse_cmd(input("> "))
        if not cmd_tup:
            continue
        cmd, r, c = cmd_tup
        if cmd == "q":
            print("Goodbye!")
            return
        if cmd in ("r", "f") and not game.in_bounds(r, c):
            print("Out of bounds.")
            continue
        if cmd == "r":
            game.reveal(r, c)
        elif cmd == "f":
            game.toggle_flag(r, c)
        print(game.render())

    print("Game over.")

if __name__ == "__main__":
    main()