import java.util.Arrays;

class Node {

    /**
     * Order of this node.
     */
    private final int ORDER;
    /**
     * Index entries of this node.
     */
    private final IndexEntry[] indexEntries;
    /**
     * Valid number of keys in this node.
     */
    private int size;
    /**
     * Children of this node.
     */
    private final Node[] children;

    /**
     * Constructor with parameter.
     * @param order order of the node
     * @param fromIndexEntries index entries to copy from
     * @param fromChildren children to copy from
     */
    public Node(int order, IndexEntry[] fromIndexEntries, Node[] fromChildren) {
        ORDER = order;
        // Index entries
        indexEntries = new IndexEntry[order]; // Extend 1 position for temporary overflow
        int size = fromIndexEntries.length;
        this.size = size;
        System.arraycopy(fromIndexEntries, 0, indexEntries, 0, size);
        // Children
        children = new Node[order + 1]; // Extend 1 position for temporary overflow
        System.arraycopy(fromChildren, 0, children, 0, fromChildren.length);
    }

    /**
     * Returns the index entries of this node.
     * @return indexEntries
     */
    public IndexEntry[] getIndexEntries() {
        return indexEntries;
    }

    /**
     * Returns the index entry at the given position.
     * @param pos position of the index entry
     * @return the i-th index entry
     */
    public IndexEntry getIndexEntry(int pos) {
        if ((pos < 0) || (pos >= size)) {
            throw new IllegalArgumentException("Invalid index entry position");
        }
        return indexEntries[pos];
    }

    /**
     * Returns the children of this node.
     * @return children
     */
    public Node[] getChildren() {
        return children;
    }

    /**
     * Returns the child at the given position.
     * @param pos index of the child
     * @return the i-th child
     */
    public Node getChild(int pos) {
        if ((pos < 0) || (pos > size)) {
            throw new IllegalArgumentException("Invalid child position");
        }
        return children[pos];
    }

    /**
     * Accessor of size.
     * @return size
     */
    public int size() {
        return size;
    }

    /**
     * Returns the maximum capacity of this node, which is 1 less than the
     * order.
     * @return capacity of this node
     */
    public int capacity() {
        return ORDER - 1;
    }

    /**
     * Returns whether this node is a leaf.
     * @return whether this node is a leaf
     */
    public boolean isLeaf() {
        return children[0] == null;
    }

    /**
     * Returns whether this node is overflowed.
     * @return whether this node is overflowed
     */
    public boolean isOverflowed() {
        return size > capacity();
    }

    /**
     * Finds the insert position for the given key, using binary search.
     * @param key key to search for
     * @return result of the binary search
     */
    public int findInsertPos(int key) {
        // Check out the documentation of Arrays.binarySearch()
        return Arrays.binarySearch(extractKeys(), 0, size, key);
    }

    /**
     * Private helper method to extract the keys from the index entries.
     * @return keys
     */
    private int[] extractKeys() {
        int[] keys = new int[size];
        for (int i = 0; i < size; ++i) {
            keys[i] = indexEntries[i].getKey();
        }
        return keys;
    }

    /**
     * Inserts the given key-record mapping into this node, at the given
     * position, with the given left and right children.
     * @param pos insert position
     * @param indexEntry index entry to insert
     * @param leftChild left child to insert
     * @param rightChild right child to insert
     */
    public void insertEntry(int pos, IndexEntry indexEntry, Node leftChild, Node rightChild) {
        // Handle the index entries
        int copyLength = size - pos;
        System.arraycopy(indexEntries, pos, indexEntries, pos + 1, copyLength);
        indexEntries[pos] = indexEntry;
        ++size;
        // Handle the children
        System.arraycopy(children, pos + 1, children, pos + 2, copyLength);
        children[pos] = leftChild;
        children[pos + 1] = rightChild;
    }

}
