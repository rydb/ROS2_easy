#FreeCad wiki:

import os
import subprocess
from dataclasses import dataclass
from abc import ABC, abstractmethod
import typing
from typing import Optional
import sys
import numpy as np
import yaml


from inspect import getsourcefile
from os.path import abspath

from ROS2_easy.classes.logger import return_logger

###
# PRE-FREECAD MACRO STARTUP AREA
###

FreeCAD = ""
def import_freecad():
    """
    function to run all steps required in order to import FreeCAD.
    
    if python integration with freecad is improved enough to allow
    `import FreeCAD` 
    with no issues, this function will
    """

try:
    import FreeCAD
    #import importDAE

except:
    
    pass




#list where packages are installed:
# https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory

#print(os.environ['HOME'])
# setup procedure if inside vscode or inside freecad:

current_env = sys.executable
macro_name = os.path.basename(__file__)

split_str = "/"
current_py_file:str = abspath(getsourcefile(lambda:0))
"""returns current file path, no clue what lambda:0 is though"""
current_py_folder = "".join([x + split_str for x in current_py_file.split(split_str)[0:-1]]) # get folder path from file path

executing_directory = os.getcwd() + "/"
"directory where this file is being executed from(should be from the directory of the project thats importing simple_run)"

###
# Config load area
###


try:
    with open("%slaunch_conf_info.yaml" % executing_directory, "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    print("urdf_file_settings.json hasn't been initialized yet. Run simple run's urdf generator once and it will generate it")
    print(os.getcwd())
    raise Exception("Actual Exception: " + str(e))


#config = yaml.load(f)

project_dir = config["PROJECT_DIR"]
#pkg = config["pkg"]
#FCStd = config["FCStd"]
urdf_name = config["URDF_NAME"]
logger = return_logger(config["LOGS_DIR"] + "urdf_converter.log", "w")

logger.info("current python interpreter is: %s" % sys.executable)

FreeCAD_mode_options = {
    "cmd": " -c ", # cmd mode is for good for fetching vars from outside scripts.
    "gui": " ", # gui mode is good for setting up enviorment vars in FreeCAD env without having to manually retype them
}
"""
dict that determines which holds which mode to launch FreeCAD in 
0 = console mode
1 = gui mode(crashes when ran. FreeCAD Does not give Verbose errors :/)
"""
FreeCAD_mode = "cmd"

"""
FREECAD WIKI FOR COMMANDS
https://wiki.freecadweb.org/Debugging#Python_Debugging
"""

if(FreeCAD == ""):
    logger.debug("script probably not executed as macro inside FreeCAD. re-running script through freecad")
    
    #runs Freecad via cmd in cmd mode and appends this macro and grabs every sys.argv after first 3 commands and adds that to command
    final_console_cmd = "freecad %s %s" % (FreeCAD_mode_options[FreeCAD_mode], current_py_file)
    os.system(final_console_cmd)

    #exit to prevent errors from FreeCAD not being defined
    exit()
    

#DEPENDENCIES FOR FREECAD MACRO
try:
            logger.warning("collada likely not installed, attempting fix using freecad.pip util that comes with snap install assuming user installed FreeCAD via snap(where error normally occurs)")
            import trimesh
            import importDAE
except:
    os.system("freecad.pip install pycollada")
    os.system("freecad.pip install trimesh")
    import importDAE
    import trimesh



@dataclass
class Material():
    """
    Represents material properties.
    
    NOTE: FreeCAD does not appear to have a innate way to give models material properties, so materials will need to be defined here.

    See: https://wiki.freecadweb.org/Material
    """
    name: str
    """name of material"""
    density: float
    """
    density of material in grams per cubic centimeter(g/cc)/(g/cm^3)
    
    get density of material from here:
    https://www.matweb.com/
    """



        
Generic_PETG = Material("PETG", 1.319)
"""'Generic' PETG. Should be the average of PETG properties"""

def unit_to_m(messure_l: list, meassure_type = "mm"):
    """
    Take all measurements in an array from `mm` and convert to `m`(by default)f

    Defaults to millitmeters since thats FreeCAD default unit for lengths.
    
    Add your measurement to measure_to_m if it isn't in there.
    """
    round_n = 6 
    measure_to_m = {
        "mm": 0.001,
    }
    multiplier = measure_to_m[meassure_type]
    
    return [round(x * multiplier, round_n) for x in messure_l]



class FreeCAD_Model_Object():
    """Abstract class with general methods needed to be defined by a given FreeCAD model type in order to interface with this program."""
    @abstractmethod
    def get_origin(self):
        """return input FreeCAD model's origin """
    @abstractmethod
    def export_self_as_dae(self):
        """export input FreeCAD model as DAE"""
    

class PartDesign_Body(FreeCAD_Model_Object):
    """
    All FreeCAD model objects that are  of type "PartDesign_body' when checked in FreeCAD.
    
    E.G: model parts Paded from sketches
    """
    def get_origin(self):
        return unit_to_m([self.model.Placement.Base[0], self.model.Placement.Base[1], self.model.Placement.Base[2]])

    def export_self_as_dae(self):
        world_origin = FreeCAD.Vector(0, 0, 0)
        old_val = self.model.Placement.Base
        self.model.Placement.Base = world_origin
        importDAE.export(self.model, self.model_dae_path)
        self.model.Placement.Base = old_val
        return self.model_dae_path

class Part_Feature(FreeCAD_Model_Object):
    def mirrored_object_base_for_origin(self):
        """
        mirrored object placement for moving the mirrored object to document origin

        I've found the formula of:
            `parent_placement - (parent_placement * (-2(-1 * normal) - 2) )`

        manages to set mirrored object's to their world origin. 
F
        """
        round_n = 6

        parent_x: float = self.model.Source.Placement.Base[0]
        normal_x: float = round(self.model.Normal[0], round_n)

        parent_y: float = self.model.Source.Placement.Base[1]
        normal_y: float = round(self.model.Normal[1], round_n)

        parent_z: float = self.model.Source.Placement.Base[2]
        normal_z: float = round(self.model.Normal[2], round_n)

        logger.debug("parents are %s" % ([parent_x, parent_y, parent_z]))
        logger.debug("parents are %s" % ([parent_x, parent_y, parent_z]))

        logger.debug("normals are %s" % [normal_x, normal_y, normal_z])
        
        base_x: float = parent_x + (parent_x * (-2 * (-1 * normal_x) - 2))
        base_y: float = parent_y + (parent_y * (-2 * (-1 * normal_y) - 2))
        base_z: float = parent_z + (parent_z * (-2 * (-1 * normal_z) - 2))

        logger.debug("base is %s" % [base_x, base_y, base_z])
        return FreeCAD.Vector(base_x, base_y, base_z)

    def export_self_as_dae(self):
            logger.debug("exporting self as dae")
            old_val = self.model.Placement.Base
            self.model.Placement.Base = Part_Feature.mirrored_object_base_for_origin(self)
            importDAE.export(self.model, self.model_dae_path)
            self.model.Placement.Base = old_val
            return self.model_dae_path

    def get_origin(self):
        round_n = 6

        flipped_normal = [round(self.model.Normal[0], round_n), round(self.model.Normal[1], round_n), round(self.model.Normal[2], round_n)]
        for i in range(0, flipped_normal.__len__()):
            if float(abs(flipped_normal[i])) == 0.0:
                flipped_normal[i] = 1
            else:
                flipped_normal[i] = flipped_normal[i] * -1
        
        #normal is a floating point array is extreme rounding errors, fix with above.

        return unit_to_m([self.model.Source.Placement.Base[0] * flipped_normal[0]\
            , self.model.Source.Placement.Base[1] * flipped_normal[1]\
                , self.model.Source.Placement.Base[2] * flipped_normal[2]])




#b.get_origin()
class Model():
    """
    Save everything relevant about them model here, and document any particular parameters here as well since FreeCAD has no IDE integration :<
    
    NOTES:
    ---
        1: FreeCAD's internal model params should NOT be saved as self. Its data clutter. Save relevant individual parts of the model like position to self though.
    """
    def __init__(self, package_dir: str, model_doc_dir: str, model_name: str, joint_type: str, ros_link_name: str, material: Material, sub_models=None, color="white"):
        self.models_folder = "%s/models/" % package_dir 
        self.urdf_folder = "%s/urdf/" % package_dir
        

        self.package_dir = package_dir
        """
        package_dir
        ---
            The root package folder which stores/will store model info/urdf info.
            E.G:
                if model_pkg is the package where model information will be stored
                then `(project_directory)/model_pkg` is package_dir
                
                models will be stored in:
                `package_dir/models`

                the created urdf file will be stored in
                `package_dir/urdf`
        """
        self.package_name = package_dir.split("/")[-2]
        self.model_doc_dir = model_doc_dir
        self.model_doc_name = model_doc_dir.split("/")[-1].replace(".FCStd", "")
        self.urdf_file = self.model_doc_name + ".xml"

        logger.debug("opening document file: |%s|" % model_doc_dir )
        self.model_doc = FreeCAD.open(model_doc_dir)
        """
        model_doc
        ---
            'Document' object inside FreeCAD which holds models. 
        """
        
        self.model = self.model_doc.findObjects(Label=model_name)[0]
        """
        model
        ---
            This is a `!!!POINTER!!!` to this model as it exists in freecad(all operations executed on this will be reflected in FreeCAD)

            when FreeCad does 'findObjects', or when refering to model variables stored in FreeCAD, this is what to reference.
        """
        if(self.model_doc.findObjects(Label=model_name).__len__() > 1):
            raise "More then 1 model found with the label %s, throwing error to prevent erros down the line" % model_name
        


        self.model_name = self.model.Label
        """Name of model's Label in FreeCAD."""
        self.material = material
        """material of model"""
        self.joint_type = joint_type
        """
        joint type in urdf E.G:
            Continous = revolves around an origin, E.G: wheel

            swivel = ???
        """
        self.ros_name = ros_link_name
        """
        ros_name:
        ---
            This is the model's name to be set inside the urdf file for links/joints and to be searched for when looking for the model in the ros2 topic list.

            to prevent ros2 simulation code from breaking because the model name changed in FreeCAD, the model's name and its ros2 link are set seperately
            E.G: if the model's name is `BaseBody`, you would want to instead input `base` for this
        """
        self.model_dae_path = "%s%s.dae" % (self.models_folder,self.ros_name)
        """path of dae export for this model"""
        self.sub_models = sub_models
        """
        all sub models of this model. 
        """

        self.center_xyz = unit_to_m([self.model.Shape.CenterOfMass[0], self.model.Shape.CenterOfMass[1], self.model.Shape.CenterOfMass[2]])
        """
        center/centroid of the model:
        ---
            SHOULD be center of mass assuming the object is of a uniform material(it will be in simulation.... probably...)
        """
        self.parents = self.model.Parents
        """
        parents:
        ---
            according to freecad, this is all parent objects which hold the current model in the deisgn
        """

        
        self.model_type: FreeCAD_Model_Object = None
        """model type which stores the specific type of model that the model exists as in FreeCAD. mirroed parts and parts extruded from pads, e.g, are not handled the same -.-"""

        if(type(self.model) == Part.Feature):
            """
            If the object is a "Part.Feature", then the model is most likely a mirrored object.

            FreeCAD does not give you the placement of a mirrored object, but you can get it from getting the "normal"/perpendicular line of the plane, and the
            position of the mirror'd object's "source"/parent object and multiplying by the opposite of the normal.

            this will give you the position of the mirrored object. 
            """
            self.model_type = Part_Feature
        else:
            logger.debug("|||PART TYPE|| part type is not if statement list. Assuming PartDesign.Body since that type cant be checked because ????")
            self.model_type = PartDesign_Body
            
        
        
        self.origin = self.model_type.get_origin(self)

        #self.export_self_as_dae = self.model_type.export_self_as_dae
        
        self.mesh_location = self.model_type.export_self_as_dae(self)
        """export mesh to dae and return its location"""
        self.mesh: trimesh.Trimesh = trimesh.load(self.mesh_location, force="mesh")
        self.mesh.density = self.material.density

    def __repr__(self):
        print("%s SPECS:" % self.model_name)
        print("=============")

        print("model center: %s " % self.center_xyz)
        print("model parents: %s" % self.parents)
        print("model origin in FreeCAD: %s" % self.origin)
        print("model document directory is: %s" % self.model_doc_dir)
        if(self.sub_models != None):
            print("model sub models: %s" % [model.model_name for model in self.sub_models])
        else:
            print("model sub models: [None]")
        return ""
        
    def symetric_inertia_tensor(self):
        """
        get "symetric" inertia tensor of model in kg/m^2

        "symetric" meaning only 6 inertia values,
        `ixx, ixy, ixz,
        iyy, iyz, izz`

        are nessecary, and not the full inertial tensor.

        See: https://classic.gazebosim.org/tutorials?tut=inertia
        """
        #helpful resource: https://towardsdatascience.com/how-to-voxelize-meshes-and-point-clouds-in-python-ca94d403f81    

        #voxelized_mesh: trimesh.voxel.VoxelGrid = mesh.voxelized(0.001)
        inertia = self.mesh.mass_properties["inertia"]
        d = 6

        #remove 'e' from number and remove inertia
        return [
            '%f' % inertia[0][0],
                '%f' % inertia[0][1],
                '%f' % inertia[0][2],
                '%f' % inertia[1][1],
                '%f' % inertia[1][2],
                '%f' % inertia[2][2]]
    def get_self_as_urdf(self):
        """
        gets relevant information about self and return a list in urdf format. This is not exporting self as urdf, that uses this to get qualites of models for exporting.
        """
        l_list = []

        l_list.append([1 ,"<link name=\"%s_link\">" % self.ros_name])
        \
            l_list.append([2, "<inertial>"])
        \
                sym_inertia = self.symetric_inertia_tensor()
        \
                pass
                #l_list.append([3, '<origin rpy="0 0 0" xyz="0.0 0.0 0.0"/>'])
        \
                l_list.append([3, '<mass value="%s"/>' % self.mesh.mass])
        \
                l_list.append([3, '<inertia ixx="%s" ixy="%s" ixz="%s" iyy="%s" iyz="%s" izz="%s"/>' % (\
                    sym_inertia[0], sym_inertia[1], sym_inertia[2], sym_inertia[3], sym_inertia[4], sym_inertia[5])])
                    #ensure inertia tensor "satisfies the triangle inequality, ie. ixx + iyy >= izz, ixx + izz >= iyy and iyy + izz >= ixx."
                    #https://physics.stackexchange.com/questions/48266/can-any-physical-rigid-body-be-represented-by-an-ellipsoid-with-the-same-angular/48273#48273
                    #https://classic.gazebosim.org/tutorials?tut=inertia    
        \
            l_list.append([2, "</inertial>"])
        \
            l_list.append([2, "<visual>"]) #VISUAL
        \
                if(self.sub_models == None): # DO NOT SET ORIGIN FOR BASE MODEL SINCE THE ORIGIN FOR THAT SHOULD STAY WHERE IT IS
                    pass
                    #l_list.append([3, "<origin xyz=\"%s %s %s\"/>" % (self.center_xyz[0], self.center_xyz[1], self.center_xyz[2])])   
        \
                l_list.append([3, "<geometry>"]) #GEOMETRY
        \
                    l_list.append([4 ,"<mesh filename=\"package://%s/models/%s.dae\"/>" % (self.package_name, self.ros_name)])
        \
                l_list.append([3, "</geometry>"])
        \
        """
                self_as_urdf.append([3, "<material>"]) #MATERIAL 
        \
                    #self_as_urdf.append([4, "<color rgba=\"%s\"/>" % self.color])
        \
                self_as_urdf.append([3, "</material>"])
        
        """
        \
            l_list.append([2, "</visual>"])
        \
        l_list.append([1, "</link>"])

        return l_list
    def export_self_as_sdf(self):
        """exports the current model and its children to sdf using gazebo.gz(gazebo snapcraft console utiltiy)'s urdf to sdf console utility """
        urdf_path = self.urdf_folder + self.urdf_file

        self.export_self_as_urdf()
        sdf_path = urdf_path + ".sdf"
        #subprocess.check_output(["gazebo.gz", "sdf -p %s > %s" % (urdf_path, sdf_path)])
        """launch model in empty gazebo world, will want to move this to simple run. Probably through editing .Json with urdf_file settings?"""
        #os.system("gazebo.gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory --reptype ignition.msgs.Boolean --timeout 1000 --req 'sdf_filename: \"%s\", name: \"urdf_model\"'" % sdf_path)


    def export_self_as_urdf(self):
        """"
        takes model and its children and converts it to an xml like list, and then transcribes it to file named after urdf_file

        then, returns the file path of the saved urdf.

        REFERENCES:
        #Sample Turtlebot3 urdf
        https://github.com/ROBOTIS-GIT/turtlebot3/blob/foxy-devel/turtlebot3_description/urdf/turtlebot3_burger.urdf

        #guide for creating a urdf
        https://docs.ros.org/en/galactic/Tutorials/Intermediate/URDF/URDF-Main.html
        """
        logger.debug("||URDF EXPORT|| exporting self as urdf..")
        #export as dae since urdf needs to read dae file
        urdf_dir = self.urdf_folder + self.urdf_file
        self_as_urdf = []
        self_as_urdf.append([0, '<robot name="diff_bot">'])
        
        #append this models link to the urdf
        for l in self.get_self_as_urdf():
            self_as_urdf.append(l)

        self_as_urdf.append(([0, '']))
        #append all sub model joints and links to the urdf
        if(self.sub_models != None):
            for sub_model in self.sub_models:
                #export sub model as dae since urdf needs to read dae file
                self_as_urdf.append([1, '<joint name="%s_joint" type="%s">' % (sub_model.ros_name, sub_model.joint_type)])
                \
                    self_as_urdf.append([2, "<origin xyz=\"%s %s %s\"/>" % (sub_model.origin[0], sub_model.origin[1], sub_model.origin[2])])
                \
                    self_as_urdf.append([2, '<parent link="%s_link"/>' % self.ros_name])
                \
                    self_as_urdf.append([2, '<child link="%s_link"/>' % sub_model.ros_name])
                \
                self_as_urdf.append([1, '</joint>'])
                self_as_urdf.append(([0, '']))
                for l in sub_model.get_self_as_urdf():
                    self_as_urdf.append(l)
                #whitespace
                self_as_urdf.append([0, ""])
            
        \
        self_as_urdf.append([0, '</robot>'])
        
        f = open(urdf_dir, "w")
        for l in self_as_urdf:
            f.write("    " * l[0] + l[1] + "\n")

        logger.info("finished exporting self ad urdf")
    def expose_paths(self):
        """
        Lists helpful debug info related to directories of things:
            1: Lists current python interpreter

            2:print all PATHs visible to the currently executing python file
        """
        print("CURRENT INTEPRETER IS: %s " % sys.executable)
        print("CURRENT PATHS ARE: ")
        print("===================")
        for p in sys.path:
            
            print(p)
    def export_self_as_GUI_commands(self):
        """
        Picking apart the API for commands requries a macro or entering commands.
        define self as a model so in a running FreeCAD instance, commands to pick apart the api can be done faster.
        """
        doc_name = "doc"
        cmd_l = []
        
        #define document
        cmd_l.append("%s = FreeCAD.getDocument('%s')" % (doc_name, self.model_doc_name))

        #define model
        cmd_l.append("%s = %s.findObjects(Label='%s')[0] " % (self.model_name, doc_name, self.model_name))

        for l in cmd_l:
            print(l)



model_pkg_dir = "%ssrc/model_pkg/" % project_dir
robot_model_path = "%ssrc/model_pkg/models/%s.FCStd" % (project_dir, urdf_name)
urdf_dir = "%ssrc/model_pkg/urdf/" % project_dir

#def generic_model_to_freecad(model:generic_model):
#    """
#    convert generic model class models into FreeCAD specific model class models
    
#    recursively traverse generic sub_models, convert them to FreeCAD models, and then, once done, return the final converted FreeCAD model
#    """
    
#    if model.sub_models != None:
#        converted_sub_model_list = []
#        for sub_model in model:
#            converted_sub_model_list.append(generic_model_to_freecad(model))
#        return Model(model.package_dir, model.robot_model_path, model.label, model.joint_type, model.ros_link_name, model.material, sub_models=converted_sub_model_list)
#    else:
#        return Model(model.package_dir, model.robot_model_path, model.label, model.joint_type, model.ros_link_name, model.material, sub_models=None)
    
    #for m in model.sub_models:
        
    #return Model(model.package_dir, model.robot_model_path, model.label, model.joint_type, model.ros_link_name, model.material, sub_models="I DONT KNOWWWWWW")

#print(robot_model_path)
#print(robot_model_path.split("/")[-1].replace(".FCStd", ""))

#wheel_left = generic_model_to_freecad(generic_model(model_pkg_dir, robot_model_path, "LeftWheel", "continuous", "left_wheel", Generic_PETG))

wheel_left = Model(model_pkg_dir, robot_model_path, "LeftWheel", "continuous", "left_wheel", Generic_PETG)
wheel_right = Model(model_pkg_dir, robot_model_path, "RightWheel", "continuous", "right_wheel", Generic_PETG)

sub_models=[wheel_left, wheel_right]
body = Model(model_pkg_dir, robot_model_path, "BodyBase", "fixed", "base", Generic_PETG, sub_models=sub_models)


body.export_self_as_urdf()

#print(model_pkg_dir)
#print(robot_model_path)
#print(urdf_dir)

exit()

