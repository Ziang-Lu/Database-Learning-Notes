import java.util.Stack;

abstract class BTreeBase {

    /**
     * Order of this B-tree or B+ tree.
     */
    protected final int ORDER;
    /**
     * Root of this B-tree or B+ tree.
     */
    protected Node root;

    /**
     * Constructor with parameter.
     * @param order order
     */
    protected BTreeBase(int order) {
        ORDER = order;
        root = null;
    }

    /**
     * Searches for the given key in this B-tree, and returns the associated
     * record address if found.
     * @param key key to search for
     * @return associated record address if found, null if not found
     */
    public String search(int key) {
        if (root == null) {
            return null;
        }
        return searchHelper(root, key);
    }

    /**
     * Private helper method to search for the given key in the given subtree
     * recursively.
     * @param curr current node
     * @param key key to search for
     * @return associated record address if found, null if not found
     */
    protected abstract String searchHelper(Node curr, int key);

    /**
     * Inserts the given key-record mapping to the B-tree.
     * @param key key to insert
     * @param recordAddress record address with the key
     */
    public void insert(int key, String recordAddress) {
        if (root == null) {
            root = new Node(ORDER, new IndexEntry[]{new IndexEntry(key, recordAddress)}, new Node[0]);
            return;
        }
        insertHelper(root, key, recordAddress, new Stack<>(), new Stack<>());
    }

    /**
     * Private helper method to insert the given key-record mapping to the given
     * subtree recursively.
     * @param curr current node
     * @param key key to insert
     * @param recordAddress record address with the key
     * @param path path along which to find the leaf
     * @param pastInsertPositions insert positions along path
     */
    private void insertHelper(Node curr, int key, String recordAddress, Stack<Node> path,
            Stack<Integer> pastInsertPositions) {
        int pos = curr.findInsertPos(key);
        if (pos >= 0) { // Found it
            // No duplicate key allowed
            return;
        }
        int insertPos = -pos - 1;
        IndexEntry indexEntry = new IndexEntry(key, recordAddress);
        if (curr.isLeaf()) { // Leaf
            // Insert into the leaf node first, and if the leaf node itself is overflowed, percolate up
            curr.insertEntry(insertPos, indexEntry, null, null);
            if (curr.isOverflowed()) {
                percolateUp(curr,i path, pastInsertPositions);
            }
            return;
        }
        // Non-leaf
        // Go to the appropriate child
        path.push(curr);
        pastInsertPositions.push(insertPos);
        insertHelper(curr.getChild(insertPos), indexEntry, path, pastInsertPositions);
    }

    /**
     * Private helper method to percolate up.
     * @param curr current node
     * @param path path along which to find the leaf
     * @param pastInsertPositions insert positions along path
     */
    protected abstract void percolateUp(Node curr, Stack<Node> path, Stack<Integer> pastInsertPositions);

}
