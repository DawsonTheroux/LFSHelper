--Author: Dawson Theroux
--Date: 15-07-2021

Description: Input an output file name and a directory and this python script will run through that directory and output the following in a text file.

	     - All unique file extentions
	     - All unique binary file extentions
	     - The git BFG command with all the of the binary file extentions.
	     - The lfs track command with all the binary file extentions.

**Note: This script will incorrectly flag files if they are encoded with UTF-16.
