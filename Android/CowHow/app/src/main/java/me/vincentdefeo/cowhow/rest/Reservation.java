package me.vincentdefeo.cowhow.rest;

import com.google.gson.annotations.Expose;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class Reservation {
    @Expose
    public String date;
    @Expose
    public String fromHour;
    @Expose
    public String toHout;
    @Expose
    public String pk;
    @Expose
    public Double lat;
    @Expose
    public Double lng;
}
