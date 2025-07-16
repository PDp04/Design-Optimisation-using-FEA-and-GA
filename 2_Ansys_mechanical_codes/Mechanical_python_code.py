

"""
Python code for Ansys Mechanical Automization
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025

This Code commands the Ansys Mechanical to insert the Directional Stresses of desired plies to study and 
then save and copy the stresses and nodes file from the Directory file to the desired location

The Directional stress involves, Sx, Sy, Sz, Sxy, Syz, Sxz for the Top, Bottom and Middle Ply


Outputs:
- stresses_load_1, stresses_load_2, stresses_load_3, stresses_load_4, stresses_load_5, stresses_load_6 folders, as there are 6 load cases

Changes:
- Change the Address where you wan to to save the file on line 237
- Change the crash variable, from which point do you wanna start your next set of dp on line 252
"""

def after_solve(this, analysis):# Do not edit this line
    """
    Called after solving the parent analysis.
    Keyword Arguments : 
        this -- the datamodel object instance of the python code object you are currently editing in the tree
        analysis -- Static Structural
    """

#============================= Finds the number of plies ======================================

    analysis = ExtAPI.DataModel.Project.Model.Analyses[0]
    solution = analysis.Solution
    
    model = ExtAPI.DataModel.Project.Model
    
    for result in solution.Children:
        if hasattr(result, "ExportToTextFile"):
            result.Delete()
            
    # Navigate to Imported Plies
    imported_plies = None
    for child in model.Children:
        if "Imported Plies" in child.Name:
            imported_plies = child
            break
     
    # Navigate to ACP (Pre)
    acp_pre = None
    if imported_plies:
        for child in imported_plies.Children:
            if "ACP (Pre)" in child.Name:
                acp_pre = child
                break
    
    # Navigate to ModelingGroup.1
    modeling_group = None
    if acp_pre:
        for child in acp_pre.Children:
            if "ModelingGroup.1" in child.Name:
                modeling_group = child
                break
    
    # Store number of plies and get the middle index
    if modeling_group:
        num_plies = len(modeling_group.Children)
        print("Number of plies in ModelingGroup.1:", num_plies)
        if num_plies > 0:
            middle_index = (num_plies + 1) // 2
            print("Middle ply index (1-based):", middle_index)
        else:
            print("No plies found in ModelingGroup.1")
    else:
        print("ModelingGroup.1 not found")

#=================Define the layers to be studied======================
    
    Layer_1 = 1
    Layer_2 = num_plies
    Layer_3 = middle_index

#=================Insert the stresses to be studied ======================
    
    #Deformation
    Deformation = solution.AddTotalDeformation()                        
    Deformation.By = SetDriverStyle.ResultSet
    
    #Sx Layer1
    Normal_stress_1 = solution.AddNormalStress()                        
    Normal_stress_1.Layer = Layer_1
    Normal_stress_1.Position = ShellFaceType.Middle
    Normal_stress_1.NormalOrientation =  NormalOrientationType.XAxis
    Normal_stress_1.By =  SetDriverStyle.ResultSet                      #Changed to ResultSet justso the load case could be changed easily
    
    #Sy Layer1
    Normal_stress_2 = solution.AddNormalStress()
    Normal_stress_2.Layer = Layer_1
    Normal_stress_2.Position = ShellFaceType.Middle
    Normal_stress_2.NormalOrientation =  NormalOrientationType.YAxis
    Normal_stress_2.By =  SetDriverStyle.ResultSet
    
    #Sz Layer1
    Normal_stress_3 = solution.AddNormalStress()
    Normal_stress_3.Layer = Layer_1
    Normal_stress_3.Position = ShellFaceType.Middle
    Normal_stress_3.NormalOrientation =  NormalOrientationType.ZAxis
    Normal_stress_3.By =  SetDriverStyle.ResultSet
    
    #Sxy Layer1
    Shear_stress_1 = solution.AddShearStress()
    Shear_stress_1.Layer = Layer_1
    Shear_stress_1.Position = ShellFaceType.Middle
    Shear_stress_1.NormalOrientation =  NormalOrientationType.XYAxis
    Shear_stress_1.By =  SetDriverStyle.ResultSet
    
    #Syz Layer1
    Shear_stress_2 = solution.AddShearStress()
    Shear_stress_2.Layer = Layer_1
    Shear_stress_2.Position = ShellFaceType.Middle
    Shear_stress_2.NormalOrientation =  NormalOrientationType.YZAxis
    Shear_stress_2.By =  SetDriverStyle.ResultSet
    
    #Sxz Layer1
    Shear_stress_3 = solution.AddShearStress()
    Shear_stress_3.Layer = Layer_1
    Shear_stress_3.Position = ShellFaceType.Middle
    Shear_stress_3.NormalOrientation =  NormalOrientationType.XZAxis
    Shear_stress_3.By =  SetDriverStyle.ResultSet
    
    #Layer2
    Normal_stress_1 = solution.AddNormalStress()
    Normal_stress_1.Layer = Layer_2
    Normal_stress_1.Position = ShellFaceType.Middle
    Normal_stress_1.NormalOrientation =  NormalOrientationType.XAxis
    Normal_stress_1.By =  SetDriverStyle.ResultSet
    
    Normal_stress_2 = solution.AddNormalStress()
    Normal_stress_2.Layer = Layer_2
    Normal_stress_2.Position = ShellFaceType.Middle
    Normal_stress_2.NormalOrientation =  NormalOrientationType.YAxis
    Normal_stress_2.By =  SetDriverStyle.ResultSet
    
    Normal_stress_3 = solution.AddNormalStress()
    Normal_stress_3.Layer = Layer_2
    Normal_stress_3.Position = ShellFaceType.Middle
    Normal_stress_3.NormalOrientation =  NormalOrientationType.ZAxis
    Normal_stress_3.By =  SetDriverStyle.ResultSet
    
    Shear_stress_1 = solution.AddShearStress()
    Shear_stress_1.Layer = Layer_2
    Shear_stress_1.Position = ShellFaceType.Middle
    Shear_stress_1.NormalOrientation =  NormalOrientationType.XYAxis
    Shear_stress_1.By =  SetDriverStyle.ResultSet
    
    Shear_stress_2 = solution.AddShearStress()
    Shear_stress_2.Layer = Layer_2
    Shear_stress_2.Position = ShellFaceType.Middle
    Shear_stress_2.NormalOrientation =  NormalOrientationType.YZAxis
    Shear_stress_2.By =  SetDriverStyle.ResultSet
    
    Shear_stress_3 = solution.AddShearStress()
    Shear_stress_3.Layer = Layer_2
    Shear_stress_3.Position = ShellFaceType.Middle
    Shear_stress_3.NormalOrientation =  NormalOrientationType.XZAxis
    Shear_stress_3.By =  SetDriverStyle.ResultSet
    
    #Layer3
    Normal_stress_1 = solution.AddNormalStress()
    Normal_stress_1.Layer = Layer_3
    Normal_stress_1.Position = ShellFaceType.Middle
    Normal_stress_1.NormalOrientation =  NormalOrientationType.XAxis
    Normal_stress_1.By =  SetDriverStyle.ResultSet
    
    Normal_stress_2 = solution.AddNormalStress()
    Normal_stress_2.Layer = Layer_3
    Normal_stress_2.Position = ShellFaceType.Middle
    Normal_stress_2.NormalOrientation =  NormalOrientationType.YAxis
    Normal_stress_2.By =  SetDriverStyle.ResultSet
    
    Normal_stress_3 = solution.AddNormalStress()
    Normal_stress_3.Layer = Layer_3
    Normal_stress_3.Position = ShellFaceType.Middle
    Normal_stress_3.NormalOrientation =  NormalOrientationType.ZAxis
    Normal_stress_3.By =  SetDriverStyle.ResultSet
    
    Shear_stress_1 = solution.AddShearStress()
    Shear_stress_1.Layer = Layer_3
    Shear_stress_1.Position = ShellFaceType.Middle
    Shear_stress_1.NormalOrientation =  NormalOrientationType.XYAxis
    Shear_stress_1.By =  SetDriverStyle.ResultSet
    
    Shear_stress_2 = solution.AddShearStress()
    Shear_stress_2.Layer = Layer_3
    Shear_stress_2.Position = ShellFaceType.Middle
    Shear_stress_2.NormalOrientation =  NormalOrientationType.YZAxis
    Shear_stress_2.By =  SetDriverStyle.ResultSet
    
    Shear_stress_3 = solution.AddShearStress()
    Shear_stress_3.Layer = Layer_3
    Shear_stress_3.Position = ShellFaceType.Middle
    Shear_stress_3.NormalOrientation =  NormalOrientationType.XZAxis
    Shear_stress_3.By =  SetDriverStyle.ResultSet
    
    #============== Solve ==== change the load case === Solve ==== Export *.txt === Move all the files to desired location====================
    import os
    
    workdir = analysis.WorkingDir
    
    # Loop through all 6 load cases
    for load_case in range(1, 7):
        # Set current load case
       # analysis.AnalysisSettings.CurrentStepNumber = load_case
    
        # Create folder name
        folder_name = "stresses_load_{0}".format(load_case)
        output_folder = os.path.join(workdir, folder_name)
    
        # Create the folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
    
        # Export each result object that supports text export
        for result in solution.Children:
            if hasattr(result, "ExportToTextFile"):
                result.SetNumber = load_case
                
        solution.EvaluateAllResults()
        
        for result in solution.Children:
            if hasattr(result, "ExportToTextFile"):
                file_name = "{0}.txt".format(result.Name)
                export_path = os.path.join(output_folder, file_name)
                result.ExportToTextFile(export_path)
    
    destination_base = r"C:\Pranav_folders\Pranav6.0"           #You Must change to the Address You wanna move all the files to

    folders_to_copy = [
        "Nodes",
        "stresses_load_1",
        "stresses_load_2",
        "stresses_load_3",
        "stresses_load_4",
        "stresses_load_5",
        "stresses_load_6"
    ]
    
    # === STEP 1: Extract dpX from workdir path and compute dp{X+309} ===
    parts = workdir.split(os.sep)
    dp_name = None
    crash = 0                                             #This is if the the Simulation crashes, you dont have to run the code again, just copy the Paramters and change here 
                                                            #so the dp will be saved in perfect order

    for part in parts:
        if part.startswith("dp") and part[2:].isdigit():
            original_index = int(part[2:])
            dp_name = "dp{}".format(original_index + crash)
            break

    
    # === STEP 2: Create destination dpX folder ===
    if dp_name is not None:
        dp_path = os.path.join(destination_base, dp_name)
        if not os.path.exists(dp_path):
            os.makedirs(dp_path)
    
        # === STEP 3: Manual folder copy ===
        def copy_folder(src_folder, dst_folder):
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            for root, dirs, files in os.walk(src_folder):
                rel_path = os.path.relpath(root, src_folder)
                target_dir = os.path.join(dst_folder, rel_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_dir, file)
                    try:
                        with open(src_file, 'rb') as fsrc:
                            with open(dst_file, 'wb') as fdst:
                                fdst.write(fsrc.read())
                    except:
                        pass  # Ignore read/write errors silently
    
        # === STEP 4: Copy listed folders ===
        for folder in folders_to_copy:
            src_path = os.path.join(workdir, folder)
            dst_path = os.path.join(dp_path, folder)
            if os.path.exists(src_path):
                copy_folder(src_path, dst_path)

    pass
