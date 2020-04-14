package common_constructs;

/**
 * B+ tree leaf class.
 * In B+ trees, these leaf nodes actually have table record addresses.
 *
 * @author Ziang Lu
 */
public class BPlusTreeLeaf extends Node {

    /**
     * Pointer to the next B+ tree leaf.
     * This is for quick and efficient in accessing all records from disks.
     */
    public BPlusTreeLeaf next;

    /**
     * Constructor with parameter
     * @param order order of this B+ tree leaf
     * @param fromIndexEntries index entries to copy from
     * @param nextLeaf next B+ tree leaf
     */
    public BPlusTreeLeaf(int order, IndexEntry[] fromIndexEntries, BPlusTreeLeaf nextLeaf) {
        super(order, fromIndexEntries, new Node[0]);
        this.next = nextLeaf;
    }

}
