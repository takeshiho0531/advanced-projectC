import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()


# metrics
def metrics(values):
    filtered_values = values[~np.isnan(values)]
    variance = np.var(filtered_values)
    std_deviation = np.std(filtered_values)
    mean = np.mean(filtered_values)
    q1 = np.percentile(filtered_values, 25)
    median = np.median(filtered_values)
    q3 = np.percentile(filtered_values, 75)
    return (variance, std_deviation, mean, q1, median, q3)


# graphs
def save_paired_distplot(values_dict, save_path):
    tcp_value_sender = values_dict["tcp_value_sender"]
    udp_100_value_sender = values_dict["udp_hundred_value_sender"]
    udp_200_value_sender = values_dict["udp_twoHundred_value_sender"]
    tcp_value_receiver = values_dict["tcp_value_receiver"]
    udp_100_value_receiver = values_dict["udp_hundred_value_receiver"]
    udp_200_value_receiver = values_dict["udp_twoHundred_value_receiver"]
    fig, (ax_above, ax_below) = plt.subplots(
        2, 3, figsize=(20, 10), sharex=True, sharey=False
    )
    ax1, ax2, ax3 = ax_above[0], ax_above[1], ax_above[2]
    ax4, ax5, ax6 = ax_below[0], ax_below[1], ax_below[2]
    sns.histplot(tcp_value_sender, kde=True, ax=ax1)
    sns.histplot(udp_100_value_sender, kde=True, ax=ax2)
    sns.histplot(udp_200_value_sender, kde=True, ax=ax3)
    sns.histplot(tcp_value_receiver, kde=True, ax=ax4)
    sns.histplot(udp_100_value_receiver, kde=True, ax=ax5)
    sns.histplot(udp_200_value_receiver, kde=True, ax=ax6)
    ax1.set_title("TCP Sender")
    ax2.set_title("UDP Sender(100Mbps)")
    ax3.set_title("UDP Sender(200Mbps)")
    ax4.set_title("TCP Receiver")
    ax5.set_title("UDP Receiver(100Mbps)")
    ax6.set_title("UDP Receiver(200Mbps)")
    plt.savefig(save_path)


def save_boxplot(values_dict, save_path):
    tcp_value_sender = values_dict["tcp_value_sender"]
    udp_100_value_sender = values_dict["udp_hundred_value_sender"]
    udp_200_value_sender = values_dict["udp_twoHundred_value_sender"]
    tcp_value_receiver = values_dict["tcp_value_receiver"]
    udp_100_value_receiver = values_dict["udp_hundred_value_receiver"]
    udp_200_value_receiver = values_dict["udp_twoHundred_value_receiver"]

    data = [
        tcp_value_sender,
        tcp_value_receiver,
        udp_100_value_sender,
        udp_100_value_receiver,
        udp_200_value_sender,
        udp_200_value_receiver,
    ]

    labels = [
        "TCP Sender",
        "TCP Receiver",
        "UDP Sender(100Mbps)",
        "UDP Receiver(100Mbps)",
        "UDP Sender(200Mbps)",
        "UDP Receiver(200Mbps)",
    ]

    fig, ax = plt.subplots(figsize=(20, 10))

    sns.boxplot(data=data, width=0.5, palette="Set3", ax=ax)

    ax.set_xticklabels(labels, rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(save_path)


# Bitrate
def convert_to_mbits_per_sec(bitrate_str):
    try:
        if pd.isnull(bitrate_str):
            return np.nan
        elif "Kbits/sec" in bitrate_str:
            bitrate_str = bitrate_str.replace("Kbits/sec", "")
            bitrate_mbit_per_sec = float(bitrate_str) / 1000
            return bitrate_mbit_per_sec
        elif "Mbits/sec" in bitrate_str:
            return bitrate_str.replace("Mbits/sec", "")
        elif "bits/sec" in bitrate_str:
            bitrate_str = bitrate_str.replace("bits/sec", "")
            bitrate_mbit_per_sec = float(bitrate_str) / 10**6
            return bitrate_mbit_per_sec

    except:
        print(bitrate_str)
        if pd.isnull(bitrate_str):
            return np.nan


def transform_bitrate_sender_df_to_values(csv_path):
    df = pd.read_csv(csv_path).drop(["file"], axis=1)
    df = df.applymap(convert_to_mbits_per_sec)
    return df.values.flatten().astype(float)


def transform_bitrate_receiver_df_to_values(csv_path):
    df = pd.read_csv(csv_path).drop(["file", "total_time"], axis=1)
    df = df.applymap(convert_to_mbits_per_sec)
    return df.values.flatten().astype(float)


def summary_bitrate_csv(
    csv_paths_dict, save_displot_path, save_boxplot_path, save_metrics_path
):
    with open(save_metrics_path, "a") as file:
        values_dict = {}
        print(csv_paths_dict)
        for key, path in csv_paths_dict.items():
            values_dict["file"] = path
            if "receiver" in key:
                values = transform_bitrate_receiver_df_to_values(path)
            elif "sender" in key:
                values = transform_bitrate_sender_df_to_values(path)
            values_dict[key] = values
            (variance, std_deviation, mean, q1, median, q3) = metrics(values)
            file.write(f"{key} \n")
            file.write(f"data number: {len(values)} \n")
            file.write(f"mean: {mean} \n")
            file.write(f"variance: {variance} \n")
            file.write(f"std_deviation: {std_deviation} \n")
            file.write(f"median: {median} \n")
            file.write(f"q1: {q1} \n")
            file.write(f"q3: {q3} \n")
            file.write("======= \n")
    save_paired_distplot(values_dict, save_displot_path)
    save_boxplot(values_dict, save_boxplot_path)


# Transfer
def convert_to_mbytes(byte_str):
    try:
        if pd.isnull(byte_str):
            return np.nan
        elif "KBytes" in byte_str:
            byte_str = byte_str.replace("KBytes", "")
            byte = float(byte_str) / 1000
            return byte
        elif "MBytes" in byte_str:
            return byte_str.replace("MBytes", "")
        elif "Bytes" in byte_str:
            byte_str = byte_str.replace("Bytes", "")
            byte = float(byte_str) / 10**6
            return byte
        else:
            print(byte_str)

    except:
        print(byte_str)
        if pd.isnull(byte_str):
            return np.nan


def transform_transfer_sender_df_to_values(csv_path):
    df = pd.read_csv(csv_path).drop(["file"], axis=1)
    df = df.applymap(convert_to_mbytes)
    for column in df:
        df[column] = df[column].values.astype(float) / (
            float(column.split("-")[1]) - float(column.split("-")[0])
        )
    return df.values.flatten().astype(float)


def transform_transfer_receiver_df_to_values(csv_path):
    df = pd.read_csv(csv_path).drop(["file"], axis=1)
    converted_df = df.drop(columns="total_time").applymap(convert_to_mbytes)
    converted_df["total_time"] = df["total_time"]
    for column in converted_df.columns:
        if column != "total_time" and column != "10.00-(11.00)":
            converted_df[column] = converted_df[column].values.astype(float) / (
                float(column.split("-")[1]) - float(column.split("-")[0])
            )
    for i in range(len(converted_df)):
        if converted_df["total_time"][i] == ">= 11.00":
            pass
        else:
            converted_df["10.00-(11.00)"][i] = float(
                converted_df["10.00-(11.00)"][i]
            ) / (float(converted_df["total_time"][i]) - 10.0)
    converted_df = converted_df.drop(columns="total_time")
    return converted_df.values.flatten().astype(float)


def summary_transfer_csv(
    csv_paths_dict, save_displot_path, save_boxplot_path, save_metrics_path
):
    print(csv_paths_dict)
    with open(save_metrics_path, "a") as file:
        values_dict = {}
        for key, path in csv_paths_dict.items():
            values_dict["file"] = path
            if "receiver" in key:
                values = transform_transfer_receiver_df_to_values(path)
            elif "sender" in key:
                values = transform_transfer_sender_df_to_values(path)
            values_dict[key] = values
            (variance, std_deviation, mean, q1, median, q3) = metrics(values)
            file.write(f"{key} \n")
            file.write(f"data number: {len(values)} \n")
            file.write(f"mean: {mean} \n")
            file.write(f"variance: {variance} \n")
            file.write(f"std_deviation: {std_deviation} \n")
            file.write(f"median: {median} \n")
            file.write(f"q1: {q1} \n")
            file.write(f"q3: {q3} \n")
            file.write("======= \n")
        print(values_dict)
    save_paired_distplot(values_dict, save_displot_path)
    save_boxplot(values_dict, save_boxplot_path)


##############################################
data_sources = ["fiveG", "wifi"]
data_types = ["Transfer", "Bitrate"]
protocols = ["tcp", "udp_hundred", "udp_twoHundred"]
directions = ["sender", "receiver"]
conditions = ["", "upperDown_"]


for data_source in data_sources:
    for condition in conditions:
        for data_type in data_types:
            csv_path_dict = {}
            if data_type == "Transfer":
                for protocol in protocols:
                    for direction in directions:
                        path = f"../../parsed/Transfer/{data_source}/{condition}{protocol}_{direction}.csv"
                        csv_path_dict[f"{protocol}_value_{direction}"] = path

                summary_transfer_csv(
                    csv_path_dict,
                    f"../results/graphs/transfer_{condition}{data_source}_displot.png",
                    f"../results/graphs/transfer_{condition}{data_source}_boxplot.png",
                    f"../results/metrics/transfer_{condition}{data_source}.txt",
                )
            elif data_type == "Bitrate":
                for protocol in protocols:
                    for direction in directions:
                        path = f"../../parsed/Bitrate/{data_source}/{condition}{protocol}_{direction}.csv"
                        csv_path_dict[f"{protocol}_value_{direction}"] = path
                summary_bitrate_csv(
                    csv_path_dict,
                    f"../results/graphs/bitrate_{condition}{data_source}_displot.png",
                    f"../results/graphs/bitrate_{condition}{data_source}_boxplot.png",
                    f"../results/metrics/bitrate_{condition}{data_source}.txt",
                )

# tc_conditions = ["bps", "delay"]
tc_conditions = ["bps"]
for tc_condition in tc_conditions:
    if tc_condition == "delay":
        protocols = ["tcp", "udp_hundred"]
    else:
        protocols = ["tcp", "udp_hundred", "udp_twoHundred"]

    for data_source in data_sources:
        for data_type in data_types:
            csv_path_dict = {}
            if data_type == "Transfer":
                for protocol in protocols:
                    for direction in directions:
                        path = f"../../parsed/Transfer/{data_source}/tc_{protocol}_{tc_condition}_{direction}.csv"
                        csv_path_dict[f"{protocol}_value_{direction}"] = path

                summary_transfer_csv(
                    csv_path_dict,
                    f"../results/graphs/tc_transfer_{tc_condition}_{data_source}_displot.png",
                    f"../results/graphs/tc_transfer_{tc_condition}_{data_source}_boxplot.png",
                    f"../results/metrics/tc_transfer_{tc_condition}_{data_source}.txt",
                )
            elif data_type == "Bitrate":
                for protocol in protocols:
                    for direction in directions:
                        path = f"../../parsed/Bitrate/{data_source}/tc_{protocol}_{tc_condition}_{direction}.csv"
                        csv_path_dict[f"{protocol}_value_{direction}"] = path
                summary_bitrate_csv(
                    csv_path_dict,
                    f"../results/graphs/tc_bitrate_{tc_condition}_{data_source}_displot.png",
                    f"../results/graphs/tc_bitrate_{tc_condition}_{data_source}_boxplot.png",
                    f"../results/metrics/tc_bitrate_{tc_condition}_{data_source}.txt",
                )
