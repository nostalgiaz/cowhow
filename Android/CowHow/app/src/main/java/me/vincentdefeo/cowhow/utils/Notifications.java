package me.vincentdefeo.cowhow.utils;

import android.app.Application;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NotificationCompat;

import me.vincentdefeo.cowhow.DetailActivity;
import me.vincentdefeo.cowhow.R;
import me.vincentdefeo.cowhow.rest.Reservation;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class Notifications {

    public static void notifyPosition(Application app, String pk, String title) {

        Reservation reservation = REST.getReservationFromPk(app, pk);

        Intent detailIntent = new Intent(app, DetailActivity.class);
        detailIntent.putExtra(DetailActivity.EXTRA, pk);

        Notification n = new NotificationCompat.Builder(app)
                .setSmallIcon(R.drawable.ic_briefcase_grey600_36dp)
                .setContentTitle(title)
                .setContentIntent(PendingIntent.getActivity(app, 0, detailIntent, 0))
                .setTicker(reservation.hostName)
                .build();

        ((NotificationManager) (app.getSystemService(Context.NOTIFICATION_SERVICE))).notify(0, n);
    }

    public static void notifyReservationStarted(Application app, String pk) {
        notifyPosition(app, pk, "Reservation Started");
    }

    public static void notifyReservationEnded(Application app, String pk) {
        notifyPosition(app, pk, "Reservation Ended");
    }
}
