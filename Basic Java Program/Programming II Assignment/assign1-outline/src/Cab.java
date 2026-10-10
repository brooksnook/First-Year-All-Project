public class Cab extends Vehicle {
    private final String driver;

    /**
     * Subclass of vehicle representing a cab
     * @param vehicleID String for the ID of the cab
     * @param fare Int for the cost of a journey
     * @param driver String for the cab's driver
     */
    public Cab(String vehicleID, int fare, String driver) {
        super(vehicleID, fare);
        this.driver = driver;
    }

    @Override
    public String toString() {
        return "Cab " + getVehicleID() + " driven by " + getDriver();
    }

    /**
     * Getter for the cab's driver
     * @return driver
     */
    public String getDriver() {
        return driver;
    }

    /**
     * Works out how much money the cab has made.
     * <p>
     * Calculated through taking the fare and multiplying it by the amount of bookings
     * @return getFare() * getBookings().size()
     */
    public int getTakings() {
        return getFare() * getBookings().size();
    }
}
