package me.vincentdefeo.cowhow.rest;

import java.util.List;

import retrofit.http.GET;
import retrofit.http.Path;
import retrofit.http.Query;

/**
 * Created by ghzmdr on 11/07/15.
 */

public interface CowHowService {
    @GET("/api/reservations")
    List<Reservation> getReservations();

    @GET("/api/reservations/{pk}")
    Reservation getReservation(@Path("pk") String pk);

    @GET("/api/coworkings")
    CoworkingResults getCoworkings(@Query("top_left") String topLeft, @Query("bottom_right") String bottomRight);
}
