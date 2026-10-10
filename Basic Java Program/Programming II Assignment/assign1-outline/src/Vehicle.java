import java.util.ArrayList;

abstract class Vehicle {
    private final String vehicleID;
    private final int fare;
    private ArrayList<Booking> bookings;

    /**
     * Abstract class for a vehicle
     * @param vehicleID String for the ID of the vehicle
     * @param fare Int for the cost of ridership
     */
    public Vehicle(String vehicleID, int fare) {
        this.vehicleID = vehicleID;
        this.fare = fare;
        this.bookings = new ArrayList<>();
    }

    /**
     * Stores a booking for the vehicle
     * @param booking The booking to be stored
     */
    public void addBooking(Booking booking) {
        bookings.add(booking);
    }

    /**
     * Getter for the vehicle ID
     * @return vehicleID
     */
    public String getVehicleID() {
        return vehicleID;
    }

    /**
     * Getter for the fare
     * @return fare
     */
    public int getFare() {
        return fare;
    }

    @Override
    public String toString() {
        return "Vehicle{" +
                "vehicleID='" + vehicleID + '\'' +
                ", fare=" + fare +
                '}';
    }

    /**
     * Getter for an ArrayList of all the vehicle's bookings
     * @return bookings
     */
    public ArrayList<Booking> getBookings() {
        return bookings;
    }

    /**
     * Abstract method that works out and then returns how much money the vehicle has made
     * @return takings
     */
    public abstract int getTakings();
}
