# DeepPacketNN
Implementation and report on the Deep Packet kit by Lotfollahi et al. (2019)

## Description
This project is a Neural Network implementation and report on a network forensics/analytics solution for classifying encrypted traffic. The project consists of two scripts and one pdf report, with all information and background being found in the latter file.

**Note: The Deep Packet Neural Network kit was NOT originally created/invented by me and is simply my program implementation of the original white paper's description of such.**

## Usage
### Preprocessing
Preprocessing must be done one packet capture at a time for each application or traffic type.
To run the preprocessing scripts, you need to first change the constant variables in the code:
- FILENAME: location of .pcap or .pcapng file to be processed
- OUTPUT_NAME: The file name of the output csv after processing
- CATEGORY_NUM: The category number of the application or traffic type (Keep track of this number, it's needed for the next program)

Now run `python3 DeepPacket_Process.py` in a terminal. This will create a csv file with the processed data in the program directory.
Join all category csv files into one file called "ApplicationData.csv" for the application classification or "TrafficData.csv" for Traffic classification.
Two sample files with this process completed are included in the repository.

### Classification
Once all processed files are completed and joined into one csv file, they can be processed into Deep Packet.
First comment/uncomment which traffic type is being analysed and then change CATEGORY_NUM to the total amount of categories for the current dataset being analysed. If you're using the provided samples, input 10 for the TrafficData.csv file and 14 for the ApplicationData.csv file.

Now run `python3 DeepPacket_NN.py` in a terminal. The program will first process the SAE and its result, then immediately move on the the CNN and its results. If you only wish to see one model at a time, simply comment the other's block of code.

## Further reading
The explanation of this project, the reason for its existence, and the article it is created from are all explained in the [Project_DeepPacket.pdf](/Project_DeepPacket.pdf) document.
