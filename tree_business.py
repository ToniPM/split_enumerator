import itertools, math


class Tree:
    def __init__(self, prescribed_node_qt, parent=None):
        self.prescribed_node_qt = prescribed_node_qt
        self.parent = parent
        self.right = None
        self.left = None
        self.label = None

        self.child_trees_are_isomorphic = False

    def __del__(self):
        try:
            if self.right is not None: del self.right
            if self.left is not None: del self.left
        except:pass

    def deepcopy(self, new_parent=None):
        copy = Tree(self.prescribed_node_qt, parent=new_parent)
        copy.left = self.left.deepcopy() if self.left is not None else None
        copy.right = self.right.deepcopy() if self.right is not None else None
        copy.child_trees_are_isomorphic = self.child_trees_are_isomorphic
        return copy

    @classmethod
    def leftmost_tree(cls, k, parent=None):
        #k is the amount of edges
        tree = Tree(k, parent=parent)
        tree.left = None if k==0 else cls.leftmost_tree(k-1, parent=tree)
        tree.right = None
        return tree

    def increment(self):
        # increments, in our tree ordering. Returns false if no increment was possible (last tree), true otherwise
        self.child_trees_are_isomorphic = False
        if self.left is None:
            # mb:
            # self.child_trees_are_isomorphic = True
            return False
        if self.left.increment():
            return True
        if self.right is not None and self.right.increment():
            left_nodes = self.left.prescribed_node_qt
            del self.left
            if left_nodes == self.right.prescribed_node_qt:
                self.left = self.right.deepcopy(new_parent=self)
                self.child_trees_are_isomorphic = True
            else:
                self.left = Tree.leftmost_tree(left_nodes, parent=self)
            return True
        if self.right is None or self.left.prescribed_node_qt>self.right.prescribed_node_qt:
            left_nodes = self.left.prescribed_node_qt
            right_nodes = -1 if self.right is None else self.right.prescribed_node_qt
            if left_nodes >= right_nodes+2:
                del self.left
                if self.right is not None: del self.right
                left_nodes -= 1
                right_nodes += 1
                self.left = Tree.leftmost_tree(left_nodes, parent=self)
                self.right = Tree.leftmost_tree(right_nodes, parent=self)
                if left_nodes == right_nodes:
                    self.child_trees_are_isomorphic = True
                return True
        return False

    def draw(self, plot, x, y, current_depth, draw_external_edges=True):
        if draw_external_edges or self.left is not None:
            plot.plot([x, x-0.49**current_depth], [y, y-1], c="black")
        if draw_external_edges or self.right is not None:
            plot.plot([x, x+0.49**current_depth], [y, y-1], c="black")
        if self.left is not None:
            self.left.draw(plot, x-0.49**current_depth, y-1, current_depth+1,
                           draw_external_edges=draw_external_edges)
        if self.right is not None:
            self.right.draw(plot, x+0.49**current_depth, y-1, current_depth+1,
                           draw_external_edges=draw_external_edges)

    def labelings(self, labels: set):
        # assert len(labels) == self.prescribed_node_qt
        qt_left = 2+(self.left.prescribed_node_qt if self.left is not None else -1)
        qt_right = 2+(self.right.prescribed_node_qt if self.right is not None else -1)
        if (self.left is None and self.right is None) or self.child_trees_are_isomorphic:
            first_label = {labels.pop()}
            qt_other_labels = qt_left - 1
            remaining_labels = labels-first_label
            left_label_assignments = (first_label.union(set(other_labels))
                                      for other_labels in itertools.combinations(remaining_labels, qt_other_labels))
        else:
            left_label_assignments = itertools.combinations(labels, qt_left)
        for left_labels in left_label_assignments:
            left_labels = set(left_labels)
            left_combinations = self.left.labelings(left_labels) if self.left is not None else [[next(iter(left_labels))]]
            right_labels = labels-left_labels
            right_combinations = self.right.labelings(right_labels) if self.right is not None else [[next(iter(right_labels))]]
            for left_assignment, right_assignment in itertools.product(left_combinations, right_combinations):
                yield left_assignment+right_assignment

    def count_labelings_below(self):
        qt_left = 2+(self.left.prescribed_node_qt if self.left is not None else -1)
        qt_right = 2+(self.right.prescribed_node_qt if self.right is not None else -1)
        label_distribution_factor = math.comb(qt_left+qt_right, qt_left)
        if (self.left is None and self.right is None) or self.child_trees_are_isomorphic:
            label_assignment_factor = 1 if self.left is None else self.left.count_labelings_below()
            total_combinations = label_distribution_factor*label_assignment_factor*label_assignment_factor//2
        else:
            label_combinations_left = 1 if self.left is None else self.left.count_labelings_below()
            label_combinations_right = 1 if self.right is None else self.right.count_labelings_below()
            total_combinations = label_distribution_factor*label_combinations_left*label_combinations_right
        return total_combinations

    def splits_below(self, qt_prior_nodes):
        if self.left is None:
            qt_prior_nodes += 1
            left_splits = []
            top_left_split = [qt_prior_nodes]
        else:
            left_splits = self.left.splits_below(qt_prior_nodes)
            top_left_split = left_splits[-1]
            qt_prior_nodes = top_left_split[-1]
        if self.right is None:
            qt_prior_nodes += 1
            right_splits = []
            top_right_split = [qt_prior_nodes]
        else:
            right_splits = self.right.splits_below(qt_prior_nodes)
            top_right_split = right_splits[-1]
        local_splits = left_splits
        local_splits.extend(right_splits)
        local_splits.append(top_left_split+top_right_split)
        return local_splits


def all_trees(k):
    tree = Tree.leftmost_tree(k)
    while True:
        yield tree.deepcopy()
        if not tree.increment(): break


def all_trees_mutable(k):
    tree = Tree.leftmost_tree(k)
    while True:
        yield tree
        if not tree.increment(): break


def relabel_split(split, relabeling):
    return [relabeling[s-1]+1 for s in split]


def relabel_splits(splits, relabeling):
    return [relabel_split(split, relabeling) for split in splits]


def format_split(split, n):
    split = set(split)
    remainder = set(range(n+1))-split
    return "".join(map(str,remainder))+"|"+"".join(map(str,split))