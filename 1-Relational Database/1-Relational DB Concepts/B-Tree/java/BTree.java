import common_constructs.IndexEntry;
import common_constructs.Node;

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
            return ((IndexEntry) curr.getEntry(pos)).getRecordAddress();
        }
        if (curr.isLeaf()) { // Leaf
            return null;
        }
        // Non-leaf
        // Go to the appropriate child
        int insertPos = -pos - 1;
        return searchHelper(curr.getChild(insertPos), key);
    }

}
