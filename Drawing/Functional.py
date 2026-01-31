from . import Drawables as dr
import Globals as g
from .DrawableProps import Sides
from . import Style

def add_rect(control, rectWidth, parent=None, parentSide=None, blockSide=None):
    return add_block(control, parent, parentSide, blockSide, rectWidth)

def add_block(control, parent=None, parentSide=None, blockSide=None, blockWidth = g.DEF_BLOCK_WIDTH):
    if parent:
        
        if parentSide:
            p = parent.get_ref_point(parentSide)
            print(p)
        else:
            p = parent.get_next_ref_point()

        block = dr.Block(posX=0, posY=0, sizeX=blockWidth, sizeY=g.DEF_BLOCK_SIZE)

        # if we specify block side, it means 
        # parent ref point CONNECTS to block on that side, so pos recalc
        if blockSide:
            block.set_pos_from_ref(p, blockSide)
            # recalculating reference points
            block.populate_ref_points()

        # block = dr.Block(posX=parent.get_ref_point(Sides.E).x, 
        #     posY=parent.get_ref_point(Sides.E).y, sizeX=g.DEF_BLOCK_SIZE, sizeY=g.DEF_BLOCK_SIZE)
        parent.attach(block)
    else:
        next_global_pos = g.global_props.get_next_pos(True)
        if next_global_pos == None:
            print ("Functional::add_block: " + "global get_next_pos() returns None!")
            return None

        block = dr.Block(posX=next_global_pos.x, posY=next_global_pos.y, \
            sizeX=blockWidth, sizeY=g.DEF_BLOCK_SIZE)

    control.add_drawable(block)
    
    return block

def add_vbar(control, parent=None):
    if not parent:
        #TODO: maybe later
        return None
    
    ref_p_south = parent.get_ref_point(Sides.S)
    if not ref_p_south:
        return None

    vbar = dr.VertBar(posX=ref_p_south.x, posY=ref_p_south.y, endX=ref_p_south.x, endY=ref_p_south.y + g.global_props.vbar_tuned_size)
    vbar.mark_ref_point_used(0)
    control.add_drawable(vbar)
    parent.attach(vbar)

    return vbar

def add_block_to_vbar(control, parent, block_width = g.DEF_BLOCK_WIDTH):
    if parent == None:
        return None
    
    vbar_rp = parent.get_next_ref_point(True)
    
    block = dr.Block(posX=0, posY=0, sizeX=block_width, sizeY=g.DEF_BLOCK_SIZE)
    block.set_pos_from_ref(vbar_rp, Sides.S)
    block.populate_ref_points()

    control.add_drawable(block)
    parent.attach(block)

    return block

def bar_to_bar(control, canvas_ctrl, src, dst, label = None):
    if src == None or dst == None:
        return None

    src_rp = src.get_next_ref_point(True)
    dst_rp = dst.get_next_ref_point(True)

    aligned = False
    while src_rp.y > dst_rp.y:
        dst_rp = dst.get_next_ref_point(True)
        if dst_rp == None:
            aligned = True
            break

    if not aligned:
        while src_rp.y < dst_rp.y:
            src_rp = src.get_next_ref_point(True)
            if src_rp == None:
                break

    if src_rp == None or dst_rp == None:
        return None
    
    connect_arrow = dr.Arrow(posX=src_rp.x, posY=src_rp.y, endX=dst_rp.x, endY=dst_rp.y)
    if label != None:
        connect_arrow.add_text(label, canvas_ctrl)

    control.add_drawable(connect_arrow)
    src.attach(connect_arrow)

    connect_arrow.mark_ref_point_used(Sides.W)
    connect_arrow.mark_ref_point_used(Sides.E)

def bar_to_iteslf(control, canvas_ctrl, send_bar, label):
    if send_bar == None:
        return None

    src_rp = send_bar.get_next_ref_point(True)
    dst_rp = send_bar.get_next_ref_point(True)

    if src_rp == None or dst_rp == None:
        return None

    # dist = 50% of dist between 2 vert bar ref points on y axis
    connect_arrow = dr.LoopedArrow(posX=src_rp.x, posY=src_rp.y, endX=dst_rp.x, endY=dst_rp.y, \
        dist=0.5 * (g.DEF_BLOCK_SIZE + g.DEF_GAP))
    
    if label != None:
        connect_arrow.add_text(label, canvas_ctrl)

    control.add_drawable(connect_arrow)
    send_bar.attach(connect_arrow)

    connect_arrow.mark_ref_point_used(Sides.W)
    connect_arrow.mark_ref_point_used(Sides.E)
    

