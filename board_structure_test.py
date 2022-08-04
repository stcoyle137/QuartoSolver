from board_structure import *
from token_structure import *



def test_dying_no_nones():
    t = TokenManager()
    c = [Cell(Coord(0,0), t.bank[0]), Cell(Coord(0,0), t.bank[2]), Cell(Coord(0,0), t.bank[1]), Cell(Coord(0,0), t.bank[12])]
    l = Line(c, 1, "c", t.attributes[0])
    l.update_health()
    assert l.die and not l.thrive and not l.alive


def test_dying_some_nones():
    t = TokenManager()
    c = [Cell(Coord(0,0), t.bank[0]), Cell(Coord(0,0), t.bank[2]), Cell(Coord(0,0), BlankToken()), Cell(Coord(0,0), t.bank[12])]
    l = Line(c, 1, "c", t.attributes[0])
    l.update_health()
    assert l.die and not l.thrive and not l.alive


def test_thriving():
    t = TokenManager()
    c = [Cell(Coord(0,0), t.bank[0]), Cell(Coord(0,0), t.bank[2]), Cell(Coord(0,0), t.bank[1]), Cell(Coord(0,0), t.bank[3])]
    l = Line(c, 1, "c", t.attributes[0])
    l.update_health()
    assert not l.die and l.thrive and not l.alive

def test_alive_with_all_same():
    t = TokenManager()
    c = [Cell(Coord(0,0), t.bank[0]), Cell(Coord(0,0), t.bank[2]), Cell(Coord(0,0), t.bank[1]), Cell(Coord(0,0), BlankToken())]
    l = Line(c, 1, "c", t.attributes[0])
    l.update_health()
    assert not l.die and not l.thrive and l.alive

def test_alive_with_all_blank():
    t = TokenManager()
    c = [Cell(Coord(0,0), BlankToken()), Cell(Coord(0,0), BlankToken()), Cell(Coord(0,0), BlankToken()), Cell(Coord(0,0), BlankToken())]
    l = Line(c, 1, "c", t.attributes[0])
    l.update_health()
    assert not l.die and not l.thrive and l.alive

def test_reap():
    t = TokenManager()
    c = [Cell(Coord(0,0), t.bank[0]), Cell(Coord(0,0), t.bank[2]), Cell(Coord(0,0), BlankToken()), Cell(Coord(0,0), t.bank[12])]
    l = Line(c, 1, "c", t.attributes[0])
    length_c = []
    for c1 in c:
        length_c.append(len(c1.lines))
    l.update_health()
    if l.die:
        l.reap()
    check = True
    for i in range(0,len(c)):
        if len(c[i].lines) == length_c[i]:
            check = False
    assert check

def test_reap_on_board():
    t = TokenManager()
    b = BoardManager(4,t)
    assert len(b.lines[4]) == 4
    b.place_token(Coord(0,0), t.bank[0])
    b.place_token(Coord(1,0), t.bank[1])
    assert len(b.lines[4]) == 3
