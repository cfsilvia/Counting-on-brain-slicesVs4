///////////////////////////////Begin the program/////////////////////////
 inputDir = getDirectory("Choose a Directory with the folder of the desired images, and ROI folder --------");
//////////////////////////////////////////////////////
File.makeDirectory(inputDir + "ROI_Into_Mask/");

title = "Choose the staining type";
Dialog.create(title);
Dialog.addChoice("Type of Staining (as oxytocin):", newArray("Cherry", "Oxytocin","Vasopresin","TH","Cfos")); //this is the name of the folder
Dialog.show();
StainCell = Dialog.getChoice();
/////////////////////////////////////
print(inputDir + StainCell + "/");
list = getFileList(inputDir + StainCell + "/");
largo=list.length;

StringyList =newArray(largo);
for(s = 0; s < largo; s++) { 
     a = substring(list[s], 0, lastIndexOf(list[s], "."));
     StringyList[s] = a; 
     }
//////////////////////////////////////////////////////
//set up the binary maske to be black inside
run("Options...", "iterations=1 count=1 black");


//loop over each file
for (i=0; i < largo; i++) {
	showProgress(i+1, list.length);	
	setBatchMode(true);
	
	print(list[i]);
	//open image
	open(inputDir + StainCell + "/"+ list[i]);
	
	rename("image");
	// create a folder for each slide with the masks
	File.makeDirectory(inputDir + "ROI_Into_Mask/" + StringyList[i] + "/");
	print(StringyList[i]);
	//open the respective ROI
	roiManager("reset");
	roiManager("open", inputDir + "ROI_From_Atlas/" + "RoiSet" + StringyList[i] + ".zip" );
    nR = roiManager("Count");  // number of ROI per image.
   print(nR);  
   //loop over every roi
   for (r = 0; r < nR; r++){ 
   	roiManager("Select", r);
   	rName = Roi.getName(); 
   	print(rName);
   	if(indexOf(rName, "/") > 0){
   		rName = replace(rName,"/","_");	
   	}
   	print(rName);
   	//convert into mask
   	run("Create Mask");
   	selectImage("Mask"); // save each mask
   	path = inputDir + "ROI_Into_Mask/" + StringyList[i] + "/" + rName + "_" + StringyList[i] + "_Mask.tif";
   	saveAs("Tiff", path);
	close();
   }
	//close image
	selectImage("image");
	close();
}
setBatchMode(false);
showMessage("Finished");