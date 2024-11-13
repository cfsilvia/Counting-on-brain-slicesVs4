//Get rois names

//directory with the rois
//inputDir = "X:/Users/Members/Silvia/From YaelK/ROI_From_Atlas_Full_Names/BMR2/ROI_From_Atlas/";
//outputFile = "X:/Users/Members/Silvia/From YaelK/FullRoiNames.xls";
//picturetoopen = "X:/Users/Members/Yael_Kashash/All Images/cfos exp/Social group/BMR2/PVN and SON_OT_cFos count/Cfos/27_BMR2_Slide1_07.tif" 

//
inputDir = "X:/Users/Members/Silvia/From YaelK/ROI_From_Atlas_Partial_Names/BMR2/ROI_From_Atlas/";
outputFile = "X:/Users/Members/Silvia/From YaelK/PartialRoiNames.xls";
picturetoopen = "X:/Users/Members/Yael_Kashash/All Images/cfos exp/Social group/BMR2/PVN and SON_OT_cFos count/Cfos/27_BMR2_Slide1_07.tif" 
open(picturetoopen); //open a randomic picture to allow code to work

//list the files inside the directory
list = getFileList(inputDir);

//loop over the files
j=1;
for(f=0; f < list.length; f++){
	//get number of slice
	number_slice = substring(list[f], 0, indexOf(list[f], "_"));
	
	//open rois
	roiManager("reset");
	roiManager("open", inputDir + list[f]);
	//loop over the rois
	nR = roiManager("Count");  // number of ROI per image.
  print(nR);     
   for (r = 0; r < nR; r++){ 
   	run("Select None");//erase previous selection
    roiManager("select",r);
    rName = Roi.getName(); 
   	//add to the table of results
   	setResult("Brain slice", j-1 ,number_slice);
    setResult("Region considered",j-1, rName);
   j=j+1;
   }
	
}
saveAs("Results",outputFile); //save the table