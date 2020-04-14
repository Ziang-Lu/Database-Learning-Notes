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
                return curr.getIndexEntry(pos).getRecordAddress();
            } else { // Not found
                return null;
            }
        }
        // Non-leaf
        // Go to the appropriate child
        int insertPos = -pos - 1;
        return searchHelper(curr.getChild(insertPos), key);
    }

    protected void percolateUp(Node curr, Stack<Node> path, Stack<Integer> pastInsertPositions) {
        // curr is overflowed
        // -> Percolate a copy of the middle key of curr
        int mid = curr.size() / 2;
        int midKey = curr.getIndexEntry(mid).getKey();
        IndexEntry upDummyEntry = new IndexEntry(midKey, null); // This dummy entry doesn't have a record address associated with it.
        Node leftChild = new Node(ORDER, Arrays.copyOfRange(curr.getIndexEntries(), 0, mid + 1),
                Arrays.copyOfRange(curr.getChildren(), 0, mid + 2));
        Node rightChild = new Node(ORDER, Arrays.copyOfRange(curr.getIndexEntries(), mid + 1, curr.size()),
                Arrays.copyOfRange(curr.getChildren(), mid + 2, curr.size() + 1));

        if (curr == root) {
            root = new Node(ORDER, new IndexEntry[]{upDummyEntry}, new Node[]{leftChild, rightChild});
            return;
        }

        // Insert into this parent node first, and if the parent node is overflowed, keep percolating up
        Node parent = path.pop();
        Integer pastInsertPos = pastInsertPositions.pop();
        parent.insertEntry(pastInsertPos, upDummyEntry, leftChild, rightChild);
        if (parent.isOverflowed()) {
            percolateUp(parent, path, pastInsertPositions);
        }
    }

}
