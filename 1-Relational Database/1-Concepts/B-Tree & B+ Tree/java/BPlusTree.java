import common_constructs.BPlusTreeLeaf;
import common_constructs.Entry;
import common_constructs.IndexEntry;
import common_constructs.Node;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Stack;

public class BPlusTree extends BTreeBase {

    private BPlusTreeLeaf leaf;
    private int leafPos;

    /**
     * Constructor with parameter.
     * @param order order of the B+ tree
     */
    public BPlusTree(int order) {
       super(order);
    }

    protected String searchHelper(Node curr, int key) {
        locateLeafAndPos(curr, key);
        if (leafPos >= 0) { // Found it
            return ((IndexEntry) leaf.getEntry(leafPos)).getRecordAddress();
        } else { // Not found
            return null;
        }
    }

    /**
     * Helper method to locate the given key in the given subtree recursively.
     * @param curr current not
     * @param key key to search for
     */
    private void locateLeafAndPos(Node curr, int key) {
        int pos = curr.findInsertPos(key);
        if (curr.isLeaf()) { // Leaf
            leaf = (BPlusTreeLeaf) curr;
            leafPos = pos;
            return;
        }
        // Non-leaf
        // Go to the appropriate child
        locateLeafAndPos(curr.getChild(pos), key);
    }

    /**
     * Searches for the given range of keys in this B+ tree, and returns the
     * associated record addresses if found.
     * @param fromKey key lower bound (inclusive)
     * @param toKey key upper bound (inclusive)
     * @return list of associated record addresses
     */
    public List<String> rangeSearch(int fromKey, int toKey) {
        if (fromKey > toKey) {
            throw new IllegalArgumentException("fromKey must be <= toKey");
        }

        if (root == null) {
            return new ArrayList<>();
        }

        // 1. Find the fromKey
        locateLeafAndPos(root, fromKey);
        // 2. Use the fact that all the leaves are connect, simply do a linear scan along the leaves (and thus the
        //    keys), find all the keys within the given range
        BPlusTreeLeaf leafPtr = leaf;
        int posPtr = leafPos;
        List<String> result = new ArrayList<>();
        while (leafPtr != null) {
            if (posPtr < leafPtr.size()) {
                IndexEntry entry = (IndexEntry) leafPtr.getEntry(posPtr);
                if (entry.getKey() > toKey) {
                    break;
                }
                result.add(entry.getRecordAddress());
                ++posPtr;
            } else {
                leafPtr = leafPtr.next;
                posPtr = 0;
            }
        }
        return result;
    }

    @Override
    protected void percolateUp(Node leaf, Stack<Node> path, Stack<Integer> pastInsertPositions) {
        // leaf is overflowed
        // -> Percolate a copy of the middle key of leaf
        int mid = leaf.size() / 2;
        int midKey = leaf.getEntry(mid).getKey();
        BPlusTreeLeaf rightChild = new BPlusTreeLeaf(ORDER,
                Arrays.copyOfRange((IndexEntry[]) leaf.getEntries(), mid, leaf.size()), null);
        BPlusTreeLeaf leftChild = new BPlusTreeLeaf(ORDER, Arrays.copyOfRange((IndexEntry[]) leaf.getEntries(), 0, mid),
                rightChild); // Connect leftChild and rightChild

        if (leaf == root) {
            root = new Node(ORDER, new Entry[]{new Entry(midKey)}, new Node[]{leftChild, rightChild});
            return;
        }

        // Insert into the parent node first, and if the parent node is overflowed, keep percolating up
        Node parent = path.pop();
        Integer pastInsertPos = pastInsertPositions.pop();
        parent.insertEntry(pastInsertPos, new Entry(midKey), leftChild, rightChild);
        BPlusTreeLeaf prevLeaf = pastInsertPos > 0 ? (BPlusTreeLeaf) parent.getChild(pastInsertPos - 1) : null;
        BPlusTreeLeaf nextLeaf = pastInsertPos < parent.size() ? (BPlusTreeLeaf) parent.getChild(pastInsertPos + 1) : null;
        if (prevLeaf != null) {
            prevLeaf.next = leftChild;
        }
        rightChild.next = nextLeaf;
        if (parent.isOverflowed()) {
            super.percolateUp(parent, path, pastInsertPositions);
        }
    }

}
