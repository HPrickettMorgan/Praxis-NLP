import os
import argparse
import glob
import random

def split_train_test(data_dir, train_out, test_out, train_test_ratio):
    pattern = os.path.join(data_dir, "*.txt")
    files = glob.glob(pattern)
    print(files)
    if files is None:
        print(f"No files matching {pattern} - try using a different data dir")

    files = sorted(files)
    random.seed(42)
    random.shuffle(files)
    train_up_to = int(len(files) * train_test_ratio)
    train_text = ""
    test_text = ""
    for i, file in enumerate(files):
        with open(file, 'r') as f:
            text = f.read()
            if i <= train_up_to:
                print(f"Appending file {os.path.basename(file)} to train")
                train_text += text
            else:
                print(f"Appending file {os.path.basename(file)} to test")
                test_text += text
    with open(train_out, 'w') as f:
        f.write(train_text)
        print(f"Written train file to {train_out}")
    with open(test_out, 'w') as f:
        f.write(test_text)
        print(f"Written test file to {test_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="Directory to get txt files from", type=str)
    parser.add_argument("train_out", help="File to output train data to")
    parser.add_argument("test_out", help="File to output test data to")

    parser.add_argument("--train_test_ratio", help="The ratio of train files to test files", default=0.8)

    args = parser.parse_args()

    split_train_test(args.data_dir, args.train_out, args.test_out, args.train_test_ratio)
