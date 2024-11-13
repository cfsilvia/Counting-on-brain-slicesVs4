//Rename Roi's files from


stringy = getDirectory("Choose a Directory with the filenames to change --------");
//////////////////////////////////////////////////////

  //Arrays made for later use.
FileList = getFileList(stringy+ "\\");

    q = FileList.length; 
  for(i = 0; i < q; i++) {
  	print(FileList[i]);
  	 nameFile = substring(FileList[i], 0, indexOf(FileList[i], "."));
  	 print(nameFile);
//  	 waitForUser("stop");
     new_nameFile = "RoiSet" + nameFile + ".zip";
    
   
//waitForUser("stop");
 
  	  print(new_nameFile);
  	//  waitForUser("stop");
  	  File.rename(stringy + FileList[i] ,stringy + new_nameFile);
  
  }

showMessage("Finished");