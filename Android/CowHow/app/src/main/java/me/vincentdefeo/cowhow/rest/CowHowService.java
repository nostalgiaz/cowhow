package me.vincentdefeo.cowhow.rest;

import java.util.List;

import retrofit.http.GET;
import retrofit.http.Path;

/**
 * Created by ghzmdr on 11/07/15.
 */

public interface CowHowService {
    @GET("/api/reservations")
    List<Reservation> getReservations();
}
