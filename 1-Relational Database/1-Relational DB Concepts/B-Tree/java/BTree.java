import java.util.Arrays;
import java.util.Stack;

public class BTree extends BTreeBase {

    /**
     * Constructor with parameter.
     * @param order order of the B-tree
     */
    public BTree(int order) {
        super(order);
    }

    protected String searchHelper(Node curr, int key) {
        int pos = curr.findInsertPos(key);
        if (pos >= 0) { // Found it
            return curr.getIndexEntry(pos).getRecordAddress();
        }
        if (curr.isLeaf()) { // Leaf
            return null;
        }
        // Non-leaf
        // Go to the appropriate child
        int insertPos = -pos - 1;
        return searchHelper(curr.getChild(insertPos), key);
    }

    protected void percolateUp(Node curr, Stack<Node> path, Stack<Integer> pastInsertPositions) {
        // curr is overflowed.
        // -> Percolate up the middle index entry of curr
        int mid = curr.size() / 2;
        IndexEntry midIndexEntry = curr.getIndexEntry(mid);
        Node leftChild = new Node(ORDER, Arrays.copyOfRange(curr.getIndexEntries(), 0, mid),
                Arrays.copyOfRange(curr.getChildren(), 0, mid + 1));
        Node rightChild = new Node(ORDER, Arrays.copyOfRange(curr.getIndexEntries(), mid + 1, curr.size()),
                Arrays.copyOfRange(curr.getChildren(), mid + 1, curr.size() + 1));

        if (curr == root) {
            root = new Node(ORDER, new IndexEntry[]{midIndexEntry}, new Node[]{leftChild, rightChild});
            return;
        }

        // Insert into this parent node first, and if the parent node is overflowed, keep percolating up
        Node parent = path.pop();
        Integer pastInsertPos = pastInsertPositions.pop();
        parent.insertEntry(pastInsertPos, midIndexEntry, leftChild, rightChild);
        if (parent.isOverflowed()) {
            percolateUp(parent, path, pastInsertPositions);
        }
    }

}
