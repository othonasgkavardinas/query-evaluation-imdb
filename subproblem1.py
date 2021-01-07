import time
#
#TITLE.BASICS.TSV
#tconst  titleType  primaryTitle  originalTitle  isAdult  startYear  endYear  runtimeMinutes  genres
#
#TITLE.AKAS.TSV
#titleId  ordering  title  region  language  types  attributes  isOriginalTitle
#
#titleId == tconst

def main():
	file_basics, file_akas, file_output = open_files()
	regions_dict = {}

	read_first_lines(file_basics, file_akas)	
	
	file_output.write("titleid\tprimaryTitle\ttitle (regions)\n")

	tokens_akas = file_akas.readline().split("\t")
	tokens_basics = file_basics.readline().split("\t")
	
	while True:
		if len(tokens_basics) == 1 or len(tokens_akas) == 1:
			break
		if tokens_basics[0] == tokens_akas[0]:
			regions_dict.clear()
			file_output.write(tokens_basics[0] + "\t" + tokens_basics[2])

			while tokens_basics[0] == tokens_akas[0]:
				if tokens_akas[2] not in regions_dict:
					regions_dict[tokens_akas[2]] = []
				regions_dict[tokens_akas[2]].append(tokens_akas[3])
				tokens_akas = file_akas.readline().split("\t")

			for key, value in regions_dict.items():
				file_output.write("\t" + key + " (")
				for i in range(len(value)):
					if i!=len(value)-1:
						file_output.write(value[i] + ",")
					else:
						file_output.write(value[i] + ")")
			file_output.write("\n")
		elif tokens_basics[0] > tokens_akas[0]:
			tokens_akas = file_akas.readline().split("\t")
		else:
			tokens_basics = file_basics.readline().split("\t")
	
	close_files(file_akas, file_basics, file_output)

def open_files():
	return (open("data/title.basics.tsv", "r"), open("data/title.akas.tsv", "r"),  open("output.tsv", "w"))

def close_files(*files):
	for file in files:
		file.close()

def read_first_lines(*files):
	for file in files:
		file.readline()

#######################################################

start_time = time.time()
main()
print("total time: %s" %(time.time() - start_time))
