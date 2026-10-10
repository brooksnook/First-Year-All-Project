import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;

public class Bus extends Vehicle {
    private ArrayList<String> route;

    /**
     * Subclass of vehicle representing a bus
     * @param vehicleID String for the ID of the bus
     * @param fare Integer for the cost per stop
     * @param route ArrayList for the bus route
     */
    public Bus(String vehicleID, int fare, ArrayList<String> route) {
        super(vehicleID, fare);
        this.route = route;
    }

    /**
     * Getter for the bus route. Represented by an array list.
     * @return route
     */
    public ArrayList<String> getRoute() {
        return route;
    }

    @Override
    public String toString() {
        return "Bus " + this.getVehicleID() + " has the route " + String.join(", ", route);
    }

    /**
     * Calculates and then returns how much money the bus made.
     * Multiplies the number of stops traveled by the fare
     * <p>
     * If final stop is after first stop, the number of stops is simply the position of the final stop minus the first
     * stop.
     * <p>
     * If the final stop is before the first stop, the bus travels to the end of the route and then to the final stop.
     * @return takings
     */
    public int getTakings() {
        int takings = 0;
        for(Booking booking : this.getBookings()) {
            int stops = 0;
            int stop1 = route.indexOf(booking.pickup());
            int stop2 = route.indexOf(booking.finalDestination());

            if(stop1 <= stop2) {
                stops = stop2 - stop1;
            } else {
                stops += route.size() - stop1;
                stops += stop2;
            }

            takings += stops * this.getFare();
        }
        return takings;
    }
}
