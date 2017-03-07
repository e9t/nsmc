import csv

with open("../ratings.txt", "r", encoding="utf-8") as tsv, open("../reviews.pos", "w") as reviews_pos, open("../reviews.neg", "w") as reviews_neg:
	tsv = csv.reader(tsv, delimiter='\t')

	for row in tsv:
			if row[2] == "1":
				reviews_pos.write(row[1] +"\n")
			elif row[2] == "0":
				reviews_neg.write(row[1] +"\n")

