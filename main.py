import itertools

from tree_business import all_trees_mutable, relabel_splits, format_split

n = 5
internal_edge_qt = n-2


def list_splits():
    for tree in all_trees_mutable(internal_edge_qt):
        splits = list(tree.splits_below(0))[:-1]
        print(" - ".join([format_split(split, n) for split in splits]),
              "(and {}-1 relabelings)".format(tree.count_labelings_below()))


def list_splits_verbose():
    for tree in all_trees_mutable(internal_edge_qt):
        labelings = list(tree.labelings(set(range(n))))
        splits = list(tree.splits_below(0))[:-1]
        for labeling in labelings:
            #print(relabel_splits(splits, labeling))
            print(" - ".join([format_split(split, n) for split in relabel_splits(splits, labeling)]))


def show_trees():
    from matplotlib import pyplot as plt
    for i,tree in enumerate(all_trees_mutable(internal_edge_qt)):
        xi, yi = i%12, i//12
        tree.draw(plt, 4*xi, -(n+1-1)*yi, 0)
    plt.show()


if __name__=="__main__":
    #show_trees()
    #list_splits()
    list_splits_verbose()