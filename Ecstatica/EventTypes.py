# coding: utf-8

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from . import Actor
from . import Part
from . import Triangle
from . import Point

class EventExecutionException(object):
    def __init__(self, routine, event_vals, what):
        self.routine = routine
        self.event_vals = event_vals
        self.what = what

def do_NO_EVENT():
    pass

def do_ROTATE(parctor, values):
    parctor.rotation = values    
   
def do_OFFSET(parctor, values):
    parctor.offset_lcl = values
    
def do_COLOUR(part, values):
    part.colour = values[0]
    
def do_VECTOR1(part, values):
    part.halfaxes = values
    
def do_VECTOR2(part, values):
    part.centre_lcl = values
    
def do_VECTOR3(part, values):
    thisfunc = do_VECTOR3 
    raise EventExecutionException(thisfunc, values, "nothing to do")

def do_ADD_PART(parctor, values):
    actor = parctor.actor
    idx = values[0]    
    newpart = actor.addPart(Part.Part(idx))
    
def do_ADD_THING(state, values):
    idx = values[0]
    actor = Actor.Actor(idx)
    state.addActor(actor)
    state.main_actor = actor    

def do_TYPE(actorpartanc, values):
    actorpartanc.typeinfo = values[0]

def do_ADD_PART_TO_THING(actor, values):    
    idx = values[0]    
    newpart = actor.addPart(Part.Part(idx))
    
def do_PSEUDO_ACTION(action, values):
    thisfunc = do_PSEUDO_ACTION 
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_PSEUDO_KEY(key, values):
    thisfunc = do_PSEUDO_KEY 
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_DISP_PNT(part, values):
    thisfunc = do_DISP_PNT 
    raise EventExecutionException(thisfunc, values, "not implemented")

def do_FLAGS(parctor, values):
    parctor.flags.clearSelected(values[1])
    parctor.flags.setSelected(values[0])
    
def do_MOVE_ACT(actor, values):
    thisfunc = do_MOVE_ACT
    raise EventExecutionException(thisfunc, values, "not implemented")

def do_RAND_ACT(values):
    thisfunc = do_RAND_ACT
    raise EventExecutionException(thisfunc, values, "not implemented")

def do_RAND_INFO(values):
    thisfunc = do_RAND_INFO
    raise EventExecutionException(thisfunc, values, "not implemented")

def do_ROTATE_THING(actor, values):
    if actor.flags['updprttrafo_uk']:
        actor.resetEndConf()
        actor.flags['updprttrafo_uk'] = False
    actor.angles = (actor.angles - actor.rotation) + values
    actor.rotation = values
    
def do_MOVE_THING(world, actor, values):
    if actor.flags['updprttrafo_uk']:
        actor.resetEndConf()
        actor.flags['updprttrafo_uk'] = False
    actor.offset_lcl = values
    diffvec = actor.matrix_2 * values
    actor.move(diffvec)
    actor.updateFlag8(world)
    
def do_START_POSITION(actor, values):
    actor.start_position = values
    
def do_THING_FLAGS(parctor, values):
    parctor.flags.overwrite(values[0])
    
def do_SCRIPT_MOVE(actor, values):
    actor.position = values
    actor.resetEndConf()
    
def do_SCRIPT_TURN(actor, values):
    actor.angles = values
    
def do_SPAWN_ACTION(game, actor, values):
    game.spawnAction(actor, values[0], values[1], values[2])
    
def do_PSEUDO_SCENE(scene, values):
    thisfunc = do_PSEUDO_SCENE 
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_PSEUDO_SCRIPT(script, values):
    thisfunc = do_PSEUDO_SCRIPT 
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_NEXT_SCENE(scene, values):
    thisfunc = do_NEXT_SCENE 
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_ANCHOR_PART(actor, part, values):
    actor.anchorPart(part)
    
def do_LOOSEN_JOINT(part, values):
    part.loosen()
    
def do_UNLOOSEN_JOINT(part, values):
    part.unloosen()

def do_POSITION(part, values):
    part.origin_lcl = values    
    
def do_2_PART_LIMB(part, values):
    part.make2PartLimb()
    
def do_FIX_PART(part, values):
    part.fix()
    
def do_UNFIX_PART(part, values):
    part.unfix()
    
def do_UNMAKE_LIMB(part, values):
    part.unmake2PartLimb()
    
def do_REORIENT_THING(actor, values):
    actor.flags['updprttrafo_uk'] = True
    
def do_PSEUDO_ADJUNCTSCENE(scene, values):
    thisfunc = do_PSEUDO_ADJUNCTSCENE
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_PSEUDO_ADJUNCT_2(adjuct, values):
    thisfunc = do_PSEUDO_ADJUNCT_2
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_ABSOLUTE_POS(part, action, values):
    part.origin_lcl = values
    if action != None and action.timemode == "abs":
        part.flags['unknown_rot_flag_200'] = True
    else:
        part.flags['unknown_rot_flag_200'] = True
        part.flags['unknown_rot_flag_4000'] = True
    
def do_ABSOLUTE_ROT(part, action, values):
    part.rotation = values
    if action != None and action.timemode == "abs":
        part.flags['unknown_rot_flag_200'] = True
    else:
        part.flags['unknown_rot_flag_200'] = True
        part.flags['unknown_rot_flag_4000'] = True
    
def do_ADD_POINT(part, values):
    idx = values[0]
    point = Point.Point(idx)
    part.addPoint(point)
    
def do_OFFSET_POINT(point, values):
    point.lcl_offset = values
    
def do_ADD_TRIANGLE(actor, idx, values):
    for v in values:
        if v < 0:
            thisfunc = do_ADD_TRIANGLE
            raise EventExecutionException(thisfunc, values, "invalid vertex index in triangle")
    triangle = Triangle.Triangle(idx)
    actor.addTriangle(triangle)
    
def do_COLOUR_TRIANGLE(triangle, values):
    triangle.front_color = values[0]
    triangle.back_color = values[1]

def do_TRIANGLE_FLAGS(triangle, values):
    #Those bit operations make no sense to me
    triangle.flags.overwrite((triangle.flags.value & (~values[1])) | (values[0] & values[1]))
    
def do_INTERACT(part, idx, values):
    if idx == 0:
        #00    INTERACT_HIT    016h    Part        FALSE        -1    Event idx        Code idx + 1                ja    nein
        pass
    elif idx == 1:
        #01    INTERACT_PICKUP    016h    Part        FALSE        -1    Event idx        Code idx + 1                ja    nein
        pass
    elif idx == 2:
        #02    INTERACT_?    016h    Part        FALSE        -1    Event idx                            ja    nein
        pass
    elif idx == 3:
        #03    INTERACT_GRABACTOR    016h    Part        FALSE        -1    Event idx        Actor idx                    ja    nein
        pass
    elif idx == 4:
        #04    INTERACT_CODE    016h    Part        FALSE        -1    Event idx        Code idx + 1                ja    nein
        pass
    elif idx == 5:
        #05    INTERACT_SOUND?    016h    Part        FALSE        -1    Event idx        Sound idx                    ja    nein
        pass

def do_POINT_TO_POINT(part, values):
    actor = part.actor    
    idx = values[0]
    if idx < 0:
        part.iktarget_uk = None #clear ik target
    else:
        part.iktarget_uk = actor.findPoint(idx)
    
def do_HELD_OFFSET(actor, values):
    actor.heldr_offset = values
    
def do_HELD_ROTATE(actor, values):
    actor.heldr_rotation = values
    
def do_BACKGROUND(actor, values):
    if values[0] == 0:
        actor.flags['unknown_flag_400'] = True
    elif values[0] == 1:
        actor.flags['unknown_flag_400'] = False        
        
def do_PSEUDO_SCENE_2(scene, values):
    thisfunc = do_PSEUDO_SCENE_2
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_PSEUDO_REPERTOIRE(repertoire, values):
    thisfunc = do_PSEUDO_REPERTOIRE
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_REP_ENTRY(repertoire, values):
    thisfunc = do_REP_ENTRY
    raise EventExecutionException(thisfunc, values, "pseudo event")

def do_ACTOR_REP(actor, values):
    actor.setRepertoireViaIdx(values[0])

def do_DEF_ROTATE(part, values):
    part.rotation_2 = values

def do_DEF_OFFSET(part, values):
    part.offset_lcl_2 = values
    
def do_DEF_VECTOR1(part, values):
    part.halfaxes_2 = values
    
def do_DEF_VECTOR2(part, values):
    part.centre_lcl_2 = values
    
def do_DEF_COLOUR(part, values):
    part.colour_2 = values

def do_DEF_FLAGS(part, values):
    part.uk_flags_2.overwrite(values[0])
    
def do_DEF_POSITION(part, values):
    part.origin_lcl_2 = values
    
def do_CUT_PART(part, values):
    part.cut()
    
def do_HELD_OFF_LEFT(actor, values):
    actor.heldl_offset = values
    
def do_HELD_ROT_LEFT(actor, values):
    actor.heldl_rotation = values

def do_THING_CODE(actor, values):
    actor.setThingCodes(values[0]-1, values[1]-1, values[2]-1)


    
