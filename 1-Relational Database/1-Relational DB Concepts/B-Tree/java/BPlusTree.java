import common_constructs.BPlusTreeLeaf;
import common_constructs.Entry;
import common_constructs.IndexEntry;
import common_constructs.Node;

import java.util.Arrays;
import java.util.Stack;

public class BPlusTree extends BTreeBase {

    /**
     * Constructor with parameter.
     * @param order order of the B+ tree
     */
    public BPlusTree(int order) {
       super(order);
    }

    protected String searchHelper(Node curr, int key) {
        int pos = curr.findInsertPos(key);
        if (curr.isLeaf()) { // Leaf
            if (pos >= 0) { // Found it
                return ((IndexEntry) curr.getEntry(pos)).getRecordAddress();
            } else { // Not found
                return null;
            }
        }
        // Non-leaf
        // Go to the appropriate child
        int insertPos = -pos - 1;
        return searchHelper(curr.getChild(insertPos), key);
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
