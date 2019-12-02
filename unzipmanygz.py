import sys
import os
import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='.')
parser.add_argument('--output_dir', default='output')

parser.add_argument('--file_type', default='.gz')
parser.add_argument('--target_str', default='com.merge.gun.shoot.zombie')
parser.add_argument('--file_prefix', default='rawlog.')
ns = parser.parse_args()


def read_gz_file(path):
    if os.path.exists(path):
        with gzip.open(path, 'r') as pf:
            for line in pf:
                yield line
    else:
        print('the path [{}] is not exist!'.format(path))


def write_json_to_file(path, file_name, data):
    file_path = os.path.join(path, file_name)
    if not os.path.exists(path):
        print('the path [{}] is not exist!'.format(path))
        answer = input("Would you like to make the dir (Y/N) ")
        if answer is "Y" or "y":
            try:
                os.mkdir(path)
            except FileExistsError:
                print("{} exist!".format(path))
        else:
            print("User Termination.")
            exit()

    with open(file_path, 'w', encoding='utf-8') as fout:
        fout.write(''.join(data))
        fout.close()


if __name__ == '__main__':
    print("get target string from large amount of files")
    b = set()
    result = []
    print(ns.input_dir)
    for root, subdirs, files in os.walk(ns.input_dir):
        for file in files:
            if '.' not in file:
                continue
            if file.startswith(ns.file_prefix) & file.endswith(ns.file_type):
                lines = read_gz_file(os.path.join(root, file))
                print(file)
                if getattr(lines, '__iter__', None):
                    for line in lines:
                        line_str = line.decode('utf-8')
                        if ns.target_str in line_str:
                            result.append(line_str)
    if result:
        output_name = "targer_" + ns.target_str.replace(".", "_") + ".json"
        write_json_to_file(ns.output_dir, output_name, result)
    else:
        print("No eligible data")