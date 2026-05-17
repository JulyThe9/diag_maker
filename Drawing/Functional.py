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

def add_vbar(control, parent=None, compLabel=None):
    if not parent:
        #TODO: parentless vbar?
        return None
    
    ref_p_south = parent.get_ref_point(Sides.S)
    if not ref_p_south:
        return None

    vbar = dr.VertBar(posX=ref_p_south.x, posY=ref_p_south.y, endX=ref_p_south.x, \
        endY=ref_p_south.y + g.global_props.vbar_tuned_size, \
        compLabel=compLabel)
        
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

def find_farthest_ref_point(vbars):
    farthest_rp = None
    for vbar in vbars:
        rp = vbar.get_next_ref_point(False)
        if rp is not None:
            if farthest_rp is None or rp.y > farthest_rp.y:
                farthest_rp = rp
    return farthest_rp

def bar_to_bar(control, canvas_ctrl, src, dst, send, recv, comm_entities, \
    label = None, extra_label = None):

    if src == None or dst == None:
        return None

    # getting all vbars from comm_entities[comp_name->dbar] dictionary
    all_vbars = list(comm_entities.values())
    try:
        farthest_rp_inbetw = find_farthest_ref_point(all_vbars)
    except Exception as e:
        if g.DEBUG:
            print(f"find_farthest_ref_point failed: {e}")
        return

    src_rp = src.get_next_ref_point(True)
    dst_rp = dst.get_next_ref_point(True)

    if farthest_rp_inbetw == None:
        return None

    # Advance src until it reaches/exceeds farthest_rp_inbetw.y
    while src_rp is not None and src_rp.y < farthest_rp_inbetw.y:
        src_rp = src.get_next_ref_point(True)

    # Advance dst until it reaches/exceeds farthest_rp_inbetw.y
    while dst_rp is not None and dst_rp.y < farthest_rp_inbetw.y:
        dst_rp = dst.get_next_ref_point(True)

    if src_rp == None or dst_rp == None:
        return None
    
    # connecting aligned src_rp and dst_rp
    connect_arrow = dr.Arrow(posX=src_rp.x, posY=src_rp.y, endX=dst_rp.x, endY=dst_rp.y)
    if label != None:
        connect_arrow.add_text(label, canvas_ctrl)
    if extra_label != None:
        connect_arrow.add_details_text(extra_label, canvas_ctrl)

    # building hierarchy
    control.add_drawable(connect_arrow)
    src.attach(connect_arrow)

    # both ref points on the arrow are marked as used
    connect_arrow.mark_ref_point_used(Sides.W)
    connect_arrow.mark_ref_point_used(Sides.E)

def bar_to_iteslf(control, canvas_ctrl, send_bar, label, extra_label):
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
    if extra_label != None:
        connect_arrow.add_details_text(extra_label, canvas_ctrl)

    control.add_drawable(connect_arrow)
    send_bar.attach(connect_arrow)

    connect_arrow.mark_ref_point_used(Sides.W)
    connect_arrow.mark_ref_point_used(Sides.E)
    

