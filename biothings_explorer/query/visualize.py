from collections import Counter
from data_tools import plotting as dtp


def display_graph(table):
    cnt = Counter()
    Row_list = []
    df = table[[item for item in table.columns if "label" in item]].drop_duplicates()
    for rows in df.itertuples():
        if len(Row_list) > 12:
            break
        if cnt[rows.output_label] < 3:
            # Create list for the current row
            my_list = list(rows)[1:]

            # append the list to the final list
            Row_list.append(my_list)

            cnt[rows.output_label] += 1
    G = dtp.build_explanitory_graph(Row_list)
    dtp.draw_explanitory_graph(G)
