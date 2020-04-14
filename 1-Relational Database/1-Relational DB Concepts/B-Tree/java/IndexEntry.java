final class IndexEntry {

    /**
     * Key of this entry.
     * Essentially, this is the primary key of the table.
     */
    private final int key;
    /**
     * Record address with the primary key.
     */
    private final String recordAddress;

    /**
     * Constructor with parameter.
     * @param key key of the entry
     * @param recordAddress record address with the key
     */
    public IndexEntry(int key, String recordAddress) {
        this.key = key;
        this.recordAddress = recordAddress;
    }

    /**
     * Accessor of key.
     * @return key
     */
    public int getKey() {
        return key;
    }

    /**
     * Accessor of recordAddress.
     * @return recordAddress
     */
    public String getRecordAddress() {
        return recordAddress;
    }

}