from scapy.all import *
import binascii
import csv

# Returns the packet at the IP header, removing everything above/prior to it
def data_link_removal(packet):
	return packet[IP]

# Converts the packet into its Hexcode form and returns an array with each byte in an index
def byte_conversion(packet):
	array = []
	hex_var = str(binascii.hexlify(bytes(packet)))[2:-1]
	for i in range(len(hex_var))[::2]:
		array.append(hex_var[i:i+2])
	return array
	
# Checks if the packet is UDP and if so, appends 12 bytes of 00 to match the 20 byte header of TCP
def transport_modification(array):
	if UDP in array:
		array = array[:28] + ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00"] + array[28:]
	return array

# Divides each byte in an array by 255 to make it either a 0 or 1 value
def normalisation(array):
	for i in range(len(array)):
		array[i] = round(int(output[i], 16)/255)
	return array
	
# Returns the given array with a full length of 1500 bytes, if it is not large enough, appends 0 until 1500 is met and then returns that
def truncation(array):
	while len(array) < 1500:
		array.append(0)
	return array[:1500]
	
# changes the source and destination ip addresses in the ip header to 0
def ip_masking(array):
	for i in range(25, 33):
		array[i] = 0
	return array

if __name__ == "__main__":
	# input pcap or pcapng file location
	filename = "filename.pcap"
	# Output name of the processed file ending in .csv
	output_filename = "filename.csv"
	# The number of category of file to be appended to the final column
	category_num = 0
	pcap = rdpcap(filename)
	with open(output_filename, 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		for packet in pcap:
			# Skips the loop if DNS, ARP, or other non-IP packet is found
			if DNS in packet or ARP in packet or IP not in packet:
				continue
			# Skips the loop if TCP packet contains either SYN, ACK, or FIN flags
			elif TCP in packet:
				if "S" in packet[TCP].flags or "A" in packet[TCP].flags or "F" in packet[TCP].flags:
					continue
			output = data_link_removal(packet)
			output = byte_conversion(output)
			output = transport_modification(output)
			output = normalisation(output)
			output = truncation(output)
			output = ip_masking(output)
			output.append(category_num)
			csvwriter.writerow(output)
