import argparse

def get_base_data():
	pinyin_data = open("data/pinyin_data").readlines()
	pinyin_table_data = open("data/拼音汉字表.txt").readlines()
	char_index_dict = eval(pinyin_data[-1])
	single_dict = eval(pinyin_data[0])
	pinyin_table_dict = {}
	for line in pinyin_table_data:
		ilist = line[0:-1].split(" ")
		pinyin_table_dict[ilist[0]] = ilist[1:]

	char_sum = 0
	for (_,v) in single_dict.items():
		char_sum += v

	lamda = 0.99
	return pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda

def dp_step(pre_char_list, pre_p_list, pinyin):
	global pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda, double_dict
	pinyin_char_list = pinyin_table_dict[pinyin]
	cur_p_list = []
	cur_char_list = []
	for pinyin_char in pinyin_char_list:
		max_p = 0
		for i in range(len(pre_char_list)):
			pre_char, pre_p = pre_char_list[i], pre_p_list[i]
			cur_p = get_p(pre_char[-1], pinyin_char) * pre_p
			if (cur_p > max_p):
				max_p = cur_p
				max_char = pre_char+pinyin_char
		cur_p_list.append(max_p)
		cur_char_list.append(max_char)
	return cur_char_list, cur_p_list

def get_p(pre_char, cur_char):
	global pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda, double_dict
	if cur_char in single_dict:
		p1 = single_dict[cur_char] / char_sum
	else:	p1 = 1 / char_sum

	p2 = 0

	if pre_char in char_index_dict:
		if pre_char not in double_dict:
			double_dict[pre_char] = eval(pinyin_data[char_index_dict[pre_char]])
		if cur_char in double_dict[pre_char]:
			p2 += double_dict[pre_char][cur_char] / single_dict[pre_char]
	return lamda * p2 + (1 - lamda) * p1

def do(pinyin_list):
	global pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda, double_dict
	cur_p_list = []
	cur_char_list = pinyin_table_dict[pinyin_list[0]]
	for char in cur_char_list:
		if char in single_dict:
			cur_p_list.append(single_dict[char] / char_sum)
		else:	cur_p_list.append(1 / char_sum)
	cur_max_p = max(cur_p_list)
	for p in cur_p_list:
		p += cur_max_p

	for pinyin in pinyin_list[1:]:
		cur_char_list, cur_p_list = dp_step(cur_char_list, cur_p_list, pinyin)

	return cur_char_list[cur_p_list.index(max(cur_p_list))]

def parser():
	global pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda, double_dict
	parser = argparse.ArgumentParser(description="将输入拼音转换为中文！")
	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument("-i", help = "输入拼音文件的路径",
		nargs = 1, dest = "input_file", type = str)
	group.add_argument("-s", help = "输入拼音字符串",
		nargs = "+", dest = "input_string", type = str)
	parser.add_argument("-o", help = "生成中文文件的储存位置",
		default = "data/output.txt", nargs = 1, dest = "out")
	args = parser.parse_args()
	return args

def main(args):
	global pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda, double_dict
	chars_list = []
	if (args.input_file != None):
		i = 0
		opath = "data/output.txt"
		if (args.out != "data/output.txt"):
			F = open(args.out[0], "w")
		F = open(opath, "w")
		for line in open(args.input_file[0]).readlines():
			F.writelines(do(line[0:-1].split(" ")) + '\n')
	else:
		print(do(args.input_string))

pinyin_data, char_index_dict, single_dict, pinyin_table_dict, char_sum, lamda= get_base_data()
double_dict = {}
if __name__ == '__main__':
	args = parser()
	main(args)
