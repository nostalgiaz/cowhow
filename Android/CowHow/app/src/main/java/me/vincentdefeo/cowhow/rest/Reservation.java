package me.vincentdefeo.cowhow.rest;

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class Reservation implements Serializable {
    @Expose
    public String date;

    @SerializedName("from_hour")
    public String fromHour;

    @SerializedName("to_hour")
    public String toHour;

    @SerializedName("host_name")
    public  String hostName;

    @Expose
    public String pk;
    @Expose
    public Double lat;
    @Expose
    public Double lng;
}
