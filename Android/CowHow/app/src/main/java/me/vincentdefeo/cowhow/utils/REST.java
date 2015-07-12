package me.vincentdefeo.cowhow.utils;

import android.app.Application;
import android.content.Context;

import com.google.android.gms.maps.model.LatLngBounds;

import java.util.List;

import me.vincentdefeo.cowhow.CowHowApplication;
import me.vincentdefeo.cowhow.rest.CoworkingResults;
import me.vincentdefeo.cowhow.rest.Reservation;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class REST {

    public static Reservation getReservationFromPk(Application a, String pk)
    {
        CowHowApplication app = (CowHowApplication) a;

        Reservation r =  app.getRestService().getReservation(pk);

        return r;
    }

    public static List<CoworkingResults.Coworking> getCoworkingsInBounds(Application a, LatLngBounds bounds)
    {
        CowHowApplication app = (CowHowApplication) a;

        String bottomRight = bounds.southwest.latitude + "," + bounds.northeast.longitude;
        String topLeft = bounds.northeast.latitude + "," + bounds.southwest.longitude;




        return app.getRestService().getCoworkings(topLeft, bottomRight).results;
    }
}
