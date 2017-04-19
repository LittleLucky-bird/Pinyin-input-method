import sys
import argparse
import os

single_dict = {}
double_dict = {}

def do(line):
	global single_dict,double_dict
	for x in line:
		if is_character(x):
			add_single(x)
			if pre_character != "":
				add_double(pre_character, x)
			pre_character = x
		else:	pre_character = ""

def add_single(x):
	global single_dict,double_dict
	if x in single_dict:
		single_dict[x] += 1
	else:
		single_dict[x] = 1
		double_dict[x] = {}

def add_double(pre_character, x):
	global single_dict,double_dict
	idict = double_dict[pre_character]
	if x in idict:
		idict[x] += 1
	else:	idict[x] = 1

def is_character(uchar):
	global single_dict,double_dict
	if '\u4e00' <= uchar<='\u9fff':
		return True
	else:	return False

def parser():
	global single_dict,double_dict
	parser = argparse.ArgumentParser(description="将语料库转化为输入法的数据！")
	parser.add_argument("-src", help = "语料库文件的位置" ,required = True,
		nargs = "+", dest = "src_dirs")
	parser.add_argument("-o", help = "生成数据的储存位置",
		default = "pinyin_data", nargs = 1, dest = "out_dir")
	args = parser.parse_args()
	return args

def corpus_file(src_dirs):
	global single_dict,double_dict
	corpus_files = []
	for x in src_dirs:
		if os.path.isfile(x):
			corpus_files.append(x)
		else:
			for y in os.listdir(x):
				if (y[0] != '.'):
					corpus_files.append(x + "/" + y)
	return set(corpus_files)

def main(args):
	global single_dict,double_dict
	corpus_files = corpus_file(args.src_dirs)
	print("共有" + str(len(corpus_files)) + "个语料文件！")
	j = 0
	for file_path in corpus_files:
		j += 1
		print("正在处理第" + str(j) + "个语料文件...")
		i = 0
		f = open(file_path)
		lines = f.readlines()
		line_num = len(lines)
		for line in lines:
			do(line)
			i += 1
			if i % 1000 == 0:
				sys.stdout.write("已经完成了" + str(i/line_num*100)[0:5] + "%." + '\r')
				sys.stdout.flush()
		print("已经完成了100.00%.")
		f.close()

	opath = "data/pinyin_data"
	if (args.out_dir != "pinyin_data"):
		opath = args.out_dir[0]
	F = open(opath,"w")
	F.write(str(single_dict))
	F.write("\n")
	position_dict = {}
	pos = 0
	for key in single_dict:
		pos += 1
		position_dict[key] = pos
		F.write(double_dict[key])
		F.write("\n")
	F.write(position_dict)

if __name__ == '__main__':
	args = parser()
	main(args)
