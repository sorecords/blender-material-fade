#################################################
#################################################
# MAKE MATERIAL FADE NODE GROUP, V 1.2
# (C) ANDREY SOKOLOV, 2019
# http://www.artstation.com/andreysokolovofficial
# This script is free for any kind of use
#################################################
#################################################
# !!! WARNING !!!
# By running this script you agree to assume all risks of using it by yourself.

# PROJECT REQUIREMENTS
# Your current Scene must have at least 1 active camera
# If you already have node groups named "Camera Range" and/or "Map Range" they will be replaced with new node groups.

# HOW TO RUN THE SCRIPT
# Open this script in Blender Text Editor
# Press RUN SCRIPT button in Blender Text Editor

# NOTHING HAPPENED!
# Script runs once to create and setup main "Camera Range" and additional "Map Range" node groups
# You can find them by pressing Shift+A => Groups in Shader Editor after running the script
# Running this script twice and more will restore default values in created groups 

# WHERE TO USE
# You may use "Camera Range" group as a Mix Factor in Mix Shader node with your main Shader and Transparent Shader plugged into it (don't forget to change Opaque to Alpha Blend in Eevee material settings)
# You may plug it to Alpha socket in Principled BSDF Shader (don't forget to change Opaque to Alpha Blend in Eevee material settings)
# You may plug Color Ramp node into it and use it for coloring your objects, depending on the distance from the camera
# You can set Cut In to 0, Fade In to 0,001, invert output and use it to make a mist in realtime

import bpy

#Setting Main Variables
Scene = bpy.context.scene
Group = bpy.data.node_groups
Camera = Scene.camera

#Setting variable for node sockets type
Value = "NodeSocketFloat"

#Setting variables for "Map Range" node group    
gr01_name = 'Map Range'
gr01_inputs = [
(Value, 'Value'),
(Value, 'Old Min'),
(Value, 'Old Max'),
(Value, 'New Min'),
(Value, 'New Max')
]
gr01_outputs = [(Value, 'Value')]

#Setting variables for "Camera Range" node group  
gr02_name = 'Camera Range'
gr02_inputs = [
(Value, 'Cut In'),
(Value, 'Fade In'),
(Value, 'Fade Out'),
(Value, 'Cut Out'),
(Value, 'Exponent In'),
(Value, 'Exponent Out')
]
gr02_outputs = [(Value, 'Value')]

#Defining Script Functions
def new_group(Name, inputs = [], outputs = [], Type = 'ShaderNodeTree',):
    '''
    If Node Group with Name doesn't exist in current Blender project:
    - Creates new Node Group with Name and Type (type is node id_name, 'ShaderNodeTree' by default)
    - Adds inputs and outputs to Node Group (empty lists by default), which can be changed by setting arguments: inputs = , outputs =
    - Places Group Input and Group Output nodes to opposite 500 units left and right from the center of Node Group
    - inputs and outputs arguments should be presented as following lists of values [(type1,name1),(type1,value2),(type2,value3)]
    - type should be a string id_name, for example 'NodeSocketFloat'
    - name should be a string, defined by user, for example 'Value'
    '''
    if not Name in Group:
        Inputs = 'Group Inputs'
        Outputs = 'Group Outputs'
        Group.new(Name,Type)
        GR_Input = Group[Name].nodes.new('NodeGroupInput')
        GR_Output = Group[Name].nodes.new('NodeGroupOutput')
        GR_Input.name = Inputs #this is node.bl_idname
        GR_Input.location = [-500,0]
        GR_Output.name = Outputs #this is node.bl_idname
        GR_Output.location = [500,0]        
        for In in inputs:
            Group[Name].inputs.new(In[0],In[1])
        for Out in outputs:
            Group[Name].outputs.new(Out[0],Out[1])

def new_node(Source, Type = 'ShaderNodeMath'):
    '''
    Adds new node with Type ('ShaderNodeMath' by default) to Source node tree.
    Source should be full path to node tree. E.g. bpy.data.node_groups['My Custom Group'],
    bpy.data.materials['MyMaterial'].node_tree
    '''
    New = Source.nodes.new(Type)
    return New
    
def link_nodes(N1,Out,N2,In,NodeGroup = 'Map Range'):
    '''
    links N1 node's Out to N2 node's In inside the NodeGroup ('Map Range' by default)
    N1, N2 - full path to nodes. E.g. bpy.data.node_groups['My Group'].nodes['Math.001']
    Out, In - int type, index of input and output starting from 0
    '''
    Group[NodeGroup].links.new(N1.outputs[Out],N2.inputs[In])

def map_range_setup(Node = 'Map Range'):
    '''
    Checks if Node ('Map Range' by default) exists, raise Assertion Error if it doesn't.
    Clears all Inputs and Outputs and recreates them with correct count, names and order.
    Removes all other nodes and recreates them with correct count, names and order.
    Links all nodes in network
    '''
    #Check if Node Group with name Node exists. Raise exception if not
    assert Node in Group
    #Set Main Group variables:
    MRange = Group[Node]
    Inputs = gr01_inputs
    Outputs = gr01_outputs
    
    #SETTING INPUTS AND OUTPUTS:
    #Rebuild Input and Output sockets structure:
    MRange.inputs.clear()
    if 'Group Inputs' not in MRange.nodes:
        Input = MRange.nodes.new('NodeGroupInput')
        Input.name = 'Group Inputs'
    for In in Inputs:
        MRange.inputs.new(In[0],In[1])
    MRange.outputs.clear()
    if 'Group Outputs' not in MRange.nodes:
        Output = MRange.nodes.new('NodeGroupOutput')
        Output.name = 'Group Outputs'
    for Out in Outputs:
        MRange.outputs.new(Out[0],Out[1])
        
    #Setting variables for Input and Output nodes:
    In = MRange.nodes['Group Inputs']
    Out = MRange.nodes['Group Outputs']
    #Setting location for Input and Output nodes:
    In.location = [-500,0]
    Out.location = [500,0]

    ### SETTING ALL OTHER NODES ###
    #CLEAR ALL NODES
    #Create list of nodes except Input and Output nodes:
    Nodes = [i for i in MRange.nodes if not i.name.startswith('Group')]
    #Delete all nodes except Group Inputs and Outputs 
    if len(Nodes) > 0:
        for N in Nodes:
            MRange.nodes.remove(N)
    
    #CREATE NEW NODES:
    #MATH
    Math = [new_node(MRange) for i in range(6)]#MRange.nodes.new('ShaderNodeMath')*6
    Math = [i for i in MRange.nodes if i.name.startswith('Math')]
    #Set their operations
    for i in Math[0:2]:
        i.operation = 'SUBTRACT'
    Math[2].operation = 'MULTIPLY'
    Math[3].operation = 'DIVIDE'
    Math[4].operation = 'SUBTRACT'
    Math[5].operation = 'ADD'
    #Set their locations
    Math[0].location = [-150,100]
    Math[1].location = [-150,50]
    Math[2].location = [-150,0]
    Math[3].location = [-150,-50]
    Math[4].location = [-150,-100]
    Math[5].location = [100,0]
    #Hide them
    for i in Math:
        i.hide = True  
    
    #LINK NODES
    link_nodes(In,0,Math[0],0)
    link_nodes(In,1,Math[0],1)
    link_nodes(In,1,Math[4],1)
    link_nodes(In,2,Math[4],0)
    link_nodes(In,3,Math[1],1)
    link_nodes(In,3,Math[5],1)
    link_nodes(In,4,Math[1],0)
    link_nodes(Math[0],0,Math[2],0)
    link_nodes(Math[1],0,Math[2],1)
    link_nodes(Math[2],0,Math[3],0)
    link_nodes(Math[4],0,Math[3],1)
    link_nodes(Math[3],0,Math[5],0)
    link_nodes(Math[5],0,Out,0)
    MRange.inputs[0].default_value = 0
    MRange.inputs[1].default_value = 0
    MRange.inputs[2].default_value = 1
    MRange.inputs[3].default_value = 0
    MRange.inputs[4].default_value = 1
    
def camera_range_setup(Node = 'Camera Range'):
    '''
    Checks if Node ('Map Range' by default) exists, raise Assertion Error if it doesn't.
    Clears all Inputs and Outputs and recreates them with correct count, names and order.
    Removes all other nodes and recreates them with correct count, names and order.
    Links all nodes in network
    Adds driver controlled by current Active Camera Clip End settings to "Camera Range" Value node inside "Camera Range" group
    '''
    #Raise Assertion Error if 'Camera Range' node-group doesn't exist:
    assert Node in Group
    #Set Main Group variables:
    CRange = Group[Node]
    Inputs = gr02_inputs
    Outputs = gr02_outputs
    
    #SETTING INPUTS AND OUTPUTS:
    #Rebuild Input and Output sockets structure:
    CRange.inputs.clear()
    if 'Group Inputs' not in CRange.nodes:
        Input = CRange.nodes.new('NodeGroupInput')
        Input.name = 'Group Inputs'
    for In in Inputs:
        CRange.inputs.new(In[0],In[1])
    CRange.outputs.clear()
    if 'Group Outputs' not in CRange.nodes:
        Output = CRange.nodes.new('NodeGroupOutput')
        Output.name = 'Group Outputs'
    for Out in Outputs:
        CRange.outputs.new(Out[0],Out[1])    
    #Setting variables for Input and Output nodes:
    In = CRange.nodes['Group Inputs']
    Out = CRange.nodes['Group Outputs']
    #Setting location for Input and Output nodes:
    In.location = [-500,-25]
    Out.location = [900,0]

    ### SETTING ALL OTHER NODES ###
    #CLEAR ALL NODES
    #Create list of nodes except Input and Output nodes:
    Nodes = [i for i in CRange.nodes if not i.name.startswith('Group')]
    #Delete all nodes except Group Inputs and Outputs:
    if len(Nodes) > 0:
        for N in Nodes:
            CRange.nodes.remove(N)
    
    #CREATE NEW NODES:
    #MATH:
    Math = [new_node(CRange) for i in range(12)]
    Math = [i for i in CRange.nodes if i.name.startswith('Math')]
    #Setting operators for Math nodes:
    for i in Math[0:5]:
        i.operation = 'DIVIDE'
    Math[5].operation = 'MULTIPLY'
    Math[6].operation = 'MINIMUM'
    Math[7].operation = 'MAXIMUM'
    Math[8].operation = 'MINIMUM'
    Math[9].operation = 'MAXIMUM'
    Math[10].operation = 'POWER'
    Math[11].operation = 'POWER'
    #Set locations of Math nodes:
    Math[0].location = [-200,100]
    Math[1].location = [-200,50]
    Math[2].location = [-200,0]
    Math[3].location = [-200,-50]
    Math[4].location = [-200,-100]
    Math[5].location = [700,0]
    Math[6].location = [220,0]
    Math[7].location = [400,0]
    Math[8].location = [220,-75]
    Math[9].location = [400,-75]
    Math[10].location = [570,-120]
    Math[11].location = [570,-170]
    Math[6].inputs[1].default_value = 1
    Math[7].inputs[1].default_value = 0
    Math[8].inputs[1].default_value = 1
    Math[9].inputs[1].default_value = 0
    #Hide all Math nodes
    for i in Math:
        i.hide = True
    
    #CAMERA DATA
    cam_data = new_node(CRange,Type = 'ShaderNodeCameraData')
    cam_data.location = [-500, 275]
    
    #VALUE FOR CAMERA RANGE
    cam_range = new_node(CRange, Type = 'ShaderNodeValue')
    cam_range.location = [-500, 125]
    cam_range.name = Node
    cam_range.label = Node
    
    #FRAME FOR DRIVED VALUE        
    scripted = new_node(CRange,Type = 'NodeFrame')
    cam_range.parent = scripted
    scripted.label = 'Camera Clip End'
    scripted.color = (0.3,0.4,0.6)
    scripted.use_custom_color = True
    
    #MAP RANGE GROUPS 
    #Raise assertion error if Map Range group node was not created
    assert 'Map Range' in Group
    
    #MAP RANGE 1
    mr_01 = CRange.nodes.new(type="ShaderNodeGroup")
    mr_01.name = 'Map Range 01'
    mr_01.node_tree = Group['Map Range']
    mr_01.hide = True
    mr_01.location = [50,0]
    
    #MAP RANGE 2
    mr_02 = CRange.nodes.new(type="ShaderNodeGroup")
    mr_02.name = 'Map Range 02'
    mr_02.node_tree = Group['Map Range']
    mr_02.hide = True
    mr_02.location = [50,-75]
    mr_02.inputs[3].default_value = 1
    mr_02.inputs[4].default_value = 0
    
    ### LINKING NODES ###   
    link_nodes(In,0,Math[1],0,NodeGroup = 'Camera Range')
    link_nodes(In,1,Math[2],0,NodeGroup = 'Camera Range')
    link_nodes(In,2,Math[3],0,NodeGroup = 'Camera Range')
    link_nodes(In,3,Math[4],0,NodeGroup = 'Camera Range')
    link_nodes(In,4,Math[10],1,NodeGroup = 'Camera Range')
    link_nodes(In,5,Math[11],1,NodeGroup = 'Camera Range')
    link_nodes(cam_data,1,Math[0],0,NodeGroup = 'Camera Range')
    link_nodes(cam_range,0,Math[0],1,NodeGroup = 'Camera Range')
    link_nodes(Math[0],0,mr_01,0,NodeGroup = 'Camera Range')
    link_nodes(Math[0],0,mr_02,0,NodeGroup = 'Camera Range')
    link_nodes(cam_range,0,Math[1],1,NodeGroup = 'Camera Range')
    link_nodes(cam_range,0,Math[2],1,NodeGroup = 'Camera Range')
    link_nodes(cam_range,0,Math[3],1,NodeGroup = 'Camera Range')
    link_nodes(cam_range,0,Math[4],1,NodeGroup = 'Camera Range')
    link_nodes(Math[1],0,mr_01,1,NodeGroup = 'Camera Range')
    link_nodes(Math[2],0,mr_01,2,NodeGroup = 'Camera Range')
    link_nodes(Math[3],0,mr_02,1,NodeGroup = 'Camera Range')
    link_nodes(Math[4],0,mr_02,2,NodeGroup = 'Camera Range')
    link_nodes(mr_01,0,Math[6],0,NodeGroup = 'Camera Range')
    link_nodes(Math[6],0,Math[7],0,NodeGroup = 'Camera Range')
    link_nodes(Math[7],0,Math[10],0,NodeGroup = 'Camera Range')
    link_nodes(Math[10],0,Math[5],0,NodeGroup = 'Camera Range')
    link_nodes(mr_02,0,Math[8],0,NodeGroup = 'Camera Range')
    link_nodes(Math[8],0,Math[9],0,NodeGroup = 'Camera Range')
    link_nodes(Math[9],0,Math[11],0,NodeGroup = 'Camera Range')
    link_nodes(Math[11],0,Math[5],1,NodeGroup = 'Camera Range')
    link_nodes(Math[5],0,Out,0,NodeGroup = 'Camera Range')
    
    #ADD CONTROLLING DRIVER FOR 'CAMERA RANGE' VALUE
    Driver = cam_range.outputs[0].driver_add('default_value').driver
    Var = Driver.variables.new()
    Var.name = 'Cam_End'
    Var.type = 'SINGLE_PROP'
    Var.targets[0].id_type = 'CAMERA'
    Var.targets[0].id = Camera.data
    Var.targets[0].data_path = 'clip_end'
    Driver.expression = Var.name

### EXECUTING ###

#Creating and setting up Map Range node group
new_group(gr01_name, inputs=gr01_inputs, outputs=gr01_outputs)
map_range_setup()
Group[gr01_name].use_fake_user = True

#Creating and setting up Camera Range node group
new_group(gr02_name, inputs=gr02_inputs, outputs=gr02_outputs)
camera_range_setup()
Cam_Range = Group[gr02_name]
Cam_Range.use_fake_user = True
Cam_Range.inputs[0].default_value = 0
Cam_Range.inputs[1].default_value = 2
Cam_Range.inputs[2].default_value = 10
Cam_Range.inputs[3].default_value = 50
Cam_Range.inputs[4].default_value = 1
Cam_Range.inputs[5].default_value = 1
