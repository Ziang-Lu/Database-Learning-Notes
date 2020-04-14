package common_constructs;

/**
 * IndexEntry class.
 * This is the class used in the nodes that actually have table record
 * addresses.
 *
 * @author Ziang Lu
 */
public final class IndexEntry extends Entry {

    /**
     * Record address with the key.
     */
    private final String recordAddress;

    /**
     * Constructor with parameter.
     * @param key key of the entry
     * @param recordAddress record address with the key
     */
    public IndexEntry(int key, String recordAddress) {
        super(key);
        this.recordAddress = recordAddress;
    }

    /**
     * Accessor of recordAddress.
     * @return recordAddress
     */
    public String getRecordAddress() {
        return recordAddress;
    }

}