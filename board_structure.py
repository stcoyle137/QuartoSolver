from token_structure import *

class Coord():
    """ x and y coorderinates storing"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.x) + ", " + str(self.y)



class Cell():
    """
    Needs to store
        - token
        - coorderinates
        - line update ids
    """

    def __init__(self, coord, token):
        self.coord = coord
        self.token = token
        self.lines = []

    def update_cell(self, token):
        update_correctly = self.update_token(token)
        if update_correctly:
            self.update_line_health()
            return True
        return False

    def update_token(self, token):
        if not self.token.whitespace:
            return False
        self.token = token
        return True

    def update_line_health(self):
        for l in self.lines:
            l.update_health()

    def check_token_attribute(self, attribute):
        for a in self.token.attribute_dict.keys():
            if a.id == -1:
                return -1
            if attribute.id == a.id:
                return self.token.attribute_dict[a]
        return None

    def is_blank(self):
        for a in self.token.attribute_dict.keys():
            if a.id == -1:
                return True
        return False
    def try_value(self, token):
        if not self.is_blank():
            return False
        self.token = token
        good = False
        for l in self.lines:
            l.update_health()
            if l.thrive:
                good = True
                break
        self.token = BlankToken()
        for l in self.lines:
            l.update_health()
        return good


    def reap_line(self, line):
        """Called when a line is dying. Remove line from the list"""
        tmp_lines = []
        for l in self.lines:
            if l.id != line.id or l.attribute != line.attribute:
                tmp_lines.append(l)
        self.lines = tmp_lines

    def __str__(self):
        if len(self.token.attribute_dict.keys()) == 1:
            return "    "
        return str(self.token)

    def __repr__(self):
        return str(self)



class Line():
    """
    Needs to Stores
        - cell idenfiers/coorinates
        - winning token
    """

    def __init__(self, cells, index, type, attribute):
        #Craetes references ('pointer') list to all cells in the line
        self.cells = cells

        #Addes reference to lines of cell
        for c in self.cells:
            c.lines.append(self)

        #Unique indenfier for a line
        self.id = index

        #Type -> either is a column (c), row (r), or diagnal(d)
        self.type = type

        #Attribute to track. Like shape, size, color, etc
        self.attribute = attribute

    def update_health(self):
        """Check for the dying, thriving or continue state"""
        self.die = False
        self.thrive = False
        self.alive = True


        tmp_cell_tok_id = []
        tmp_is_all_player = True
        tm_player_tok_id = []
        for c in self.cells:
            tmp_a_id = c.check_token_attribute(self.attribute)
            if tmp_a_id == None:
                raise Exception("Something went wrong in the lines/cell class. An attribute does not exist or something. IDK you're the programmer, figure it out")
            if tmp_a_id == -1:
                tmp_is_all_player = False
            else:
                tm_player_tok_id += [c.check_token_attribute(self.attribute)]
            tmp_cell_tok_id += [c.check_token_attribute(self.attribute)]
        if(len(set(tmp_cell_tok_id)) == 1 and tmp_is_all_player):
            self.thrive = True
            self.alive = False
            return
        elif(len(set(tm_player_tok_id)) > 1):
            self.die = True
            self.alive = False
            return
        else:
            self.die = False
            self.thrive = False
            self.alive = True

    def reap(self):
        """Terminates the line and removes references from the associated cells"""
        for c in self.cells:
            c.reap_line(self)

    def __str__(self):
        cells_str = []
        for c in self.cells:
            cells_str.append(str(c))
        return " " + " | ".join(cells_str) + "\n"

    def __repr__(self):
        return str(list)



class BoardManager():
    def __init__(self, dim, token_manager):
        self.board = [[Cell(Coord(i, j), BlankToken()) for j in range(dim)] for i in range(dim)]
        self.dim = dim
        self.possible_attributes = token_manager.attributes
        self.lines = {}
        self.won = False
        self.alive = True
        self.lines_tot = self.dim * len(self.possible_attributes)


        self.lines = {r : {a : self.lineify_row(r, 0, a) for a in self.possible_attributes} for r in range(self.dim)}
        self.lines.update({c + self.dim : {a : self.lineify_col(c, self.dim, a) for a in self.possible_attributes} for c in range(self.dim)})
        self.lines.update({d + 2 * self.dim : {a : self.lineify_dia(d, 2 * self.dim, a) for a in self.possible_attributes} for d in range(2)})

    def place_token(self, coord, token):
        if (coord.x >= self.dim or coord.x < 0) or (coord.y >= self.dim or coord.y < 0):
            return False

        if not self.board[coord.x][coord.y].update_cell(token):
            return False

        self.update_state(self.board[coord.x][coord.y])
        return True

    def update_state(self, cell):
        to_reap = []
        for line in cell.lines:
            if line.die:
                to_reap += [(line.id, line.attribute)]
            if line.thrive:
                self.won = True
        for reaper in to_reap:
            self.lines[reaper[0]].pop(reaper[1]).reap()
            if len(self.lines[reaper[0]]) == 0:
                self.lines.pop(reaper[0])
        if len(self.lines) == 0:
            self.alive = False


    def lineify_row(self, row_num, offset, attribute):
        """Returns an array representing a certain 'row' in the board
            @param row, row number - Restrictions 0-'n'
        """
        return Line(self.board[row_num], row_num + offset, "r", attribute)

    def lineify_col(self, col_num, offset, attribute):
        """Returns an array representing a certain 'col' in the board
            @param col, column number - Restrictions 0-'n'
        """
        return Line([self.board[i][col_num] for i in range(self.dim)], col_num + offset, "c", attribute)

    def lineify_dia(self, dia_num, offset, attribute):
        """Returns an array representing 'dia' diagonal in the board
            @param dia, diagonal number - Restrictions 0-1

            Upper Left to Lower Right is 0
            Upper Right to Lower Left is 1
            Example
             0      1
                01
             1      0
        """
        if(dia_num not in [0, 1]):
            return
        return Line([self.board[dia_num*(self.dim - 2*i - 1) + i][i] for i in range(self.dim)], dia_num + offset, "d", attribute)

    def stringify_row(self, row):
        """DO NOT USE. BAD PROGRAMMER, BAD!"""
        strRows = " "
        for c in self.board[row]:
            strRows += str(c)
            strRows += " | "
        return strRows[0: len(strRows)-2] + "\n"

    def get_valid_placements(self):
        list_valid = []
        for l in self.board:
            for c in l:
                if c.is_blank():
                    list_valid.append(c.coord)
        return list_valid

    def __str__(self):
        strRows = [self.stringify_row(r) for r in range(self.dim)]
        horizBar = "------" * self.dim + "-" * (self.dim - 1) + "\n"
        return horizBar.join(strRows)
