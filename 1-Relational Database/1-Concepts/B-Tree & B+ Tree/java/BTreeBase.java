import common_constructs.Entry;
import common_constructs.IndexEntry;
import common_constructs.Node;

import java.util.Arrays;
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
            // No duplicate key allowed to be inserted
            return;
        }
        int insertPos = -pos - 1;
        if (curr.isLeaf()) { // Leaf
            // Insert into the leaf node first, and if the leaf node itself is overflowed, percolate up
            curr.insertEntry(insertPos, new IndexEntry(key, recordAddress), null, null);
            if (curr.isOverflowed()) {
                percolateUp(curr, path, pastInsertPositions);
            }
            return;
        }
        // Non-leaf
        // Go to the appropriate child
        path.push(curr);
        pastInsertPositions.push(insertPos);
        insertHelper(curr.getChild(insertPos), key, recordAddress, path, pastInsertPositions);
    }

    /**
     * Private helper method to percolate up.
     * @param curr current node
     * @param path path along which to find the leaf
     * @param pastInsertPositions insert positions along path
     */
    protected void percolateUp(Node curr, Stack<Node> path, Stack<Integer> pastInsertPositions) {
        // curr is overflowed.
        // -> Percolate up the middle index entry of curr
        int mid = curr.size() / 2;
        Entry midEntry = curr.getEntry(mid);
        Node leftChild = new Node(ORDER, Arrays.copyOfRange(curr.getEntries(), 0, mid),
                Arrays.copyOfRange(curr.getChildren(), 0, mid + 1));
        Node rightChild = new Node(ORDER, Arrays.copyOfRange(curr.getEntries(), mid + 1, curr.size()),
                Arrays.copyOfRange(curr.getChildren(), mid + 1, curr.size() + 1));

        if (curr == root) {
            root = new Node(ORDER, new Entry[]{midEntry}, new Node[]{leftChild, rightChild});
            return;
        }

        // Insert into this parent node first, and if the parent node is overflowed, keep percolating up
        Node parent = path.pop();
        Integer pastInsertPos = pastInsertPositions.pop();
        parent.insertEntry(pastInsertPos, midEntry, leftChild, rightChild);
        if (parent.isOverflowed()) {
            BTreeBase.this.percolateUp(parent, path, pastInsertPositions);
        }
    }

}
