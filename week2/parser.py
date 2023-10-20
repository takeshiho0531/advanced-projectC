import os

import pandas as pd


def separate_sender_receiver_lines(file_path):
    lines = []
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                lines.append(line)
            if len(lines) <= 0:
                return
            if lines[-1] != "iperf Done.\n":
                return
            if "Server output:\n" in lines:
                index = lines.index("Server output:\n")
                sender_lines = lines[:index]
                receiver_lines = lines[index + 1 :]  # noqa
                return [sender_lines, receiver_lines]

    except FileNotFoundError:
        print(f"cannot find file: {file_path}")
    except Exception as e:
        print(f"error occurred: {str(e)}")


def make_sender_dict(sender_lines, file_path):
    file_name = os.path.basename(file_path)
    found_interval = False
    found_separator = False
    info = {}
    info["file"] = file_name

    for line in sender_lines:
        if "Interval" in line:
            found_interval = True
        elif "- - - - - -" in line:
            found_separator = True
        elif found_interval and not found_separator:
            info_list = line.split()
            sec_index = info_list.index("sec")
            if sec_index > 0:
                time = info_list[sec_index - 1]
            else:
                continue
            transfer = None
            for i in range(1, len(info_list)):
                if "Bytes" in info_list[i]:
                    transfer = info_list[i - 1] + info_list[i]
                    info[time] = transfer
                    break
    return info


def make_receiver_dict(receiver_lines, file_path):
    file_name = os.path.basename(file_path)
    found_interval = False
    found_separator = False
    info = {}
    info["file"] = file_name

    for line in receiver_lines:
        if "Interval" in line:
            found_interval = True
        elif "- - - - - -" in line:
            found_separator = True
        elif found_interval and not found_separator:
            info_list = line.split()
            sec_index = info_list.index("sec")
            if sec_index > 0:
                time = info_list[sec_index - 1]
            else:
                continue
            transfer = None
            found_ten_second = False
            for i in range(1, len(info_list)):
                if "10.00-" in info_list[i]:
                    found_ten_second = True
                if (not found_ten_second) and "Bytes" in info_list[i]:
                    transfer = info_list[i - 1] + info_list[i]
                    info[time] = transfer
                transfer = None
                if found_ten_second and "Bytes" in info_list[i]:
                    transfer = info_list[i - 1] + info_list[i]
                    info["10.00-"] = transfer
                    info["total_time"] = time.split("10.00-")[1]
                    break
    return info


def make_dataframe(directory_path):
    file_list = os.listdir(directory_path)
    text_file_paths = []
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        if file_name.endswith(".txt"):
            text_file_paths.append(file_path)

    sender_dicts_list = []
    receiver_dict_list = []

    for file_path in text_file_paths:
        try:
            info = separate_sender_receiver_lines(file_path)

            if not info:
                continue
            sender_lines = info[0]
            receiver_lines = info[1]

            sender_dict = make_sender_dict(sender_lines, file_path)
            receiver_dict = make_receiver_dict(receiver_lines, file_path)

            sender_dicts_list.append(sender_dict)
            receiver_dict_list.append(receiver_dict)
        except:  # noqa
            continue
    return sender_dicts_list, receiver_dict_list


def save_csv(data_directory_path, saved_parent_directory_path):
    assert data_directory_path.startswith(("./fiveG/", "./wifi/"))

    if not saved_parent_directory_path.endswith("/"):
        saved_parent_directory_path += "/"

    splitted_data_directory = data_directory_path.split("/")
    if len(splitted_data_directory) < 3:
        print("invelid directory path")
        return

    save_base_path = (
        saved_parent_directory_path
        + splitted_data_directory[1]
        + "/"
        + ("_".join(splitted_data_directory[2:]))
    )

    sender_dicts_list, receiver_dict_list = make_dataframe(data_directory_path)

    save_sender_path = save_base_path + "_sender.csv"
    save_receiver_path = save_base_path + "_receiver.csv"

    (pd.DataFrame(sender_dicts_list)).to_csv(save_sender_path, index=False)
    (pd.DataFrame(receiver_dict_list)).to_csv(save_receiver_path, index=False)


def get_deepest_subdirectories(root_dir):
    subdirectories = [f.path for f in os.scandir(root_dir) if f.is_dir()]
    deepest_subdirectories = []
    if not subdirectories:
        return [root_dir]
    for subdir in subdirectories:
        deepest_subdirectories.extend(get_deepest_subdirectories(subdir))
    return deepest_subdirectories


try:
    os.makedirs("./parsed/fiveG", exist_ok=False)
except FileExistsError:
    print("Directory ./parsed/fiveG already exists.")
try:
    os.makedirs("./parsed/wifi", exist_ok=False)
except FileExistsError:
    print("Directory ./parsed/wifi already exists.")

# Local5G
for subdir in get_deepest_subdirectories("./fiveG/"):
    save_csv(subdir, "./parsed/")
# wifi
for subdir in get_deepest_subdirectories("./wifi/"):
    save_csv(subdir, "./parsed/")
