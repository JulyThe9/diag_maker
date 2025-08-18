import Drawables as dr
import Globals as g
from DrawableProps import Sides
import Style

def add_test(control):
    block1 = dr.Block(posX=g.global_props.get_next_pos().x, posY=g.global_props.get_next_pos().y, sizeX=50, sizeY=50)
    control.add_drawable(block1)  

    connect_p = block1.get_ref_point(Sides.E, update=True)
    posX = connect_p.x
    posY = connect_p.y

    arrow1 = dr.Arrow(posX=posX, posY=posY, endX=posX+100, endY=posY)

    print(arrow1.props.ref_points)

    control.add_drawable(arrow1)

    block1.attach(arrow1)
    arrow1.mark_ref_point_used(Sides.W)

    posX = arrow1.posX + arrow1.sizeX

    arrow1.mark_ref_point_used(Sides.E)
    # TODO: moving NON-horizontal line is NOT IMPLEMENTED
    arrow2 = dr.Arrow(posX=posX, posY=posY, endX=posX+100, endY=posY)
    control.add_drawable(arrow2)

    arrow1.attach(arrow2)
    arrow2.mark_ref_point_used(Sides.W)

    blockS = block1.get_ref_point(Sides.S)
    vbar = dr.VertBar(posX=blockS.x, posY=blockS.y, endX=blockS.x, endY=blockS.y+500)
    control.add_drawable(vbar)
    block1.attach(vbar)

    return arrow2

def add_block(control, parent=None, parentSide=None, blockSide=None):
    if not parent == None:
        
        if parentSide:
            p = parent.get_ref_point(parentSide)
            print(p)
        else:
            p = parent.get_next_ref_point()

        block = dr.Block(posX=p.x, posY=p.y, sizeX=50, sizeY=50)

        # if we specify block side, it means 
        # parent ref point CONNECTS to block on that side, so pos recalc
        if blockSide:
            block.set_pos_from_ref(p, blockSide)

        # block = dr.Block(posX=parent.get_ref_point(Sides.E).x, 
        #     posY=parent.get_ref_point(Sides.E).y, sizeX=50, sizeY=50)
        parent.attach(block)
    else:
        block = dr.Block(posX=g.global_props.get_next_pos().x, posY=g.global_props.get_next_pos().y, sizeX=50, sizeY=50)
    control.add_drawable(block)
