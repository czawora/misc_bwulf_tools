
import argparse
import os
import glob
import shutil

# parse args
parser = argparse.ArgumentParser(description='')

parser.add_argument('subj_path')
parser.add_argument('dest_path')
parser.add_argument('--clean_subj', action='store_true')
parser.add_argument('--clean_lfp', action='store_true')
parser.add_argument('--clean_sort', action='store_true')
parser.add_argument('--clean_safety', action='store_true')
parser.add_argument('--copy_lfp', action='store_true')
parser.add_argument('--copy_sort', action='store_true')
parser.add_argument('--copy_safety', action='store_true')

args = parser.parse_args()

subj_path = args.subj_path
dest_path = args.dest_path
clean_subj = args.clean_subj
clean_lfp = args.clean_lfp
clean_sort = args.clean_sort
clean_safety = args.clean_safety
copy_lfp = args.copy_lfp
copy_sort = args.copy_sort
copy_safety = args.copy_safety

if os.path.isdir(subj_path) is False:
	print(subj_path + " is not a valid path")
	exit(1)

if os.path.isdir(dest_path) is False:
	print(dest_path + " is not a valid path")
	exit(1)

if copy_lfp is False and copy_sort is False and clean_subj is False and clean_sort is False and clean_lfp is False:

	print("no action chosen")

else:

	###########################################################
	###########################################################
	# copy

	if copy_lfp is True or copy_sort is True:

		copy_pairs = []

		if copy_safety is True:
			print("(safety)", end="")
		print("(copy) searching " + subj_path + " ... ")

		for sess in glob.glob(subj_path + "/*"):

			dest_sess_path = dest_path + "/" + sess

			if copy_lfp is True:

				for f in glob.glob(sess + "/lfp/outputs/microDev*") + glob.glob(sess + "/lfp/outputs/variance.csv"):

					print(f)
					copy_pairs.append((f, dest_sess_path + "/cleaning"))

				for f in glob.glob(sess + "/lfp/outputs/*processed.mat") + glob.glob(sess + "/lfp/outputs/*noreref.mat"):

					print(f)
					copy_pairs.append((f, dest_sess_path + "/raw"))


			if copy_sort is True:

				for f in glob.glob(sess + "/spike/outputs/*sortSummary.csv") + glob.glob(sess + "/spike/outputs/*spikeWaveform.mat") + glob.glob(sess + "/spike/outputs/*sortFigs"):

					print(f)
					copy_pairs.append((f, dest_sess_path + "/sorting"))

				for f in glob.glob(sess + "/spike/outputs/*spikeInfo.mat"):

					print(f)
					copy_pairs.append((f, dest_sess_path + "/raw"))

		if copy_safety is True:
			print("(safety)", end="")
		print("(copy) copying " + str(len(copy_pairs)) + " items to " + dest_path  + " ... ")

		copied = 0
		for cp in copy_pairs:

			if copy_safety is True:
				print("(safety)", end="")
			print("(copy) " + str(copied) + " of " + str(len(copy_pairs)) + " " + cp[0] + " --> " + cp[1])

			shutil.copytree(cp[0], cp[1])
			copied += 1

	###########################################################
	###########################################################
	# delete

	if clean_subj is True or clean_sort is True or clean_lfp is True:

		if clean_safety is True:
			print("(safety)", end="")
		print("(delete) searching " + subj_path + " ... ")

		if clean_subj is True:

			paths = glob.glob(subj_path + "/*")

		else:

			paths = []

			if clean_lfp is True:

				paths += glob.glob(subj_path + "/*/lfp")

			if clean_sort is True:

				paths += glob.glob(subj_path + "/*/spike")

		if clean_safety is True:
			print("(safety)", end="")
		print("Found " + str(len(paths)) + " directories to delete ")

		if clean_safety is True:
			print("(safety)", end="")
		resp = input("Are you sure you want to delete these items ? y/[n]")

		if resp == "y":

			if clean_safety is True:
				print("(safety)", end="")
			print("(delete) deleting " + " ... ")

			deleted = 0
			for p in paths:

				if clean_safety is True:
					print("(safety)", end="")
				print("(delete) " + str(deleted) + " of " + str(len(paths)) + ": " + p)

				shutil.rmtree(p)
				deleted += 1