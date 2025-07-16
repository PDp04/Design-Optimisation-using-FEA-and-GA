Follow Step By Step

- Step1: Go to '0_Python_Preprocessing_sobol_code' folder to the 'Parameter_Generator.py' amd run the code

- Step2: Open the generated 'sobol_composites_10_to_100_plies.csv' file, 
	there the CSV generated won't have all the values, will have to input the dp no. and the Extrusion, Angle1, Angle2 using excel.

	Or directly use the generated .csv file, given in the folder
	and while copying to Ansys, make sure you replace TRUE with 'True and FALSE with 'False, or it will show error

- Step3: Go to '1_Simulation_File' and open the 'Ansys_stresses.wbpj'

- Step4: Copy and paste the Parameters Generated using 'Parameter_Generator.py' 

- Step5: Go to '2_Ansys_mechanical_codes' and verify the 'Mechanical_APDL_code.txt' in 
	Project 
	  → Model (C2) 
	    → Static Structural (C3) 
	      → Solution (C4) 
	        → Commands (APDL)
	And verify the 'Mechanical_python_code.py' in 
	Project 
	  → Model (C2) 
	    → Static Structural (C3) 
	      → Solution (C4) 
	        → Python Code
	in that change the Directory as stated, where ever you want your solutions. Set the 'crash' to 0 if starting a new or else set the ongoing dp, helpful when Ansys Crashes
	For Example:
		if My ansys crashes after 309 paramters, as the output data is already in your directory, so no need to run everything again
		just delete the dp and start fresh by copying from 310th dp and just change the crash to 309
		
	and start the Simulation by 'Update all Design Points'

- Step6: Go to '3_Python_post_preparation_codes' folder, and run Code '1_Extract.py' and '2_Input_preparation.py'. They can be run simultaneously and even in steps. 

- Step7: Before Running the '3_Combination.py' code make sure you read the instrusctions given in the code, i.e. make the folders as follows
        Component_stresses/
        ├── load1                           
        ├── load2
        ├── load3 
        ├── load4 
        ├── load5
        └── load6
	After the folders are created, run the code by giving the address. I know, this could be done just by code, but that was accedently got skipped

- Step8: Go to '4_Python_post_processing_Code' folder and run the codes one by one by following the instruction in the code.

- Step9: You will get the Optimized solution folders, there is no stop function yet but can be added in the future





	 