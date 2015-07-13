package me.vincentdefeo.cowhow.utils;

import android.content.Context;
import android.location.Geocoder;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;

import java.io.IOException;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class Maps {

    public static String getAddressFromCoords(Context c, double lat, double lng) {
        String address = null;
        Geocoder g = new Geocoder(c);

        try {
            address = g.getFromLocation(lat, lng, 1).get(0).getAddressLine(0);
        } catch (IOException e) {
            e.printStackTrace();
            address = lat + " " + lng;
        }

        return address;
    }

    public static void getMapImage(Context c, double lat, double lng, ImageView imageView)
    {
        String url = "https://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lng + "zoom=13&size=600x400&maptype=roadmap&markers=color:red%7C"+ lat + "," + lng;
        Picasso.with(c).load(url).into(imageView);
    }
}
