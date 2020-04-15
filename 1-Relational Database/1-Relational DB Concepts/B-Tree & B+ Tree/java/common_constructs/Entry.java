package common_constructs;

/**
 * Entry class.
 * This is the class used in each node.
 *
 * @author Ziang Lu
 */
public class Entry {

    /**
     * Key of this entry.
     * Essentially, this is the primary key of the table.
     */
    private final int key;

    /**
     * Constructor with parameter.
     * @param key key of the entry
     */
    public Entry(int key) {
        this.key = key;
    }

    /**
     * Accessor of key.
     * @return key
     */
    public int getKey() {
        return key;
    }

}
