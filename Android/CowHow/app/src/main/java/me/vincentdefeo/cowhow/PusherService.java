package me.vincentdefeo.cowhow;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import com.pusher.client.Pusher;
import com.pusher.client.channel.Channel;
import com.pusher.client.channel.SubscriptionEventListener;

import me.vincentdefeo.cowhow.utils.Notifications;

public class PusherService extends Service {

    final static String PUSHER_API_KEY = "45656fd4d10dc8df4bdc";

    final static String chanName = "COWORKINGS";

    final static String startEventName = "START_EVENT";
    final static String endEventName = "END_EVENT";

    Pusher push;
    Channel chan;

    public PusherService()
    {
        push = new Pusher(PUSHER_API_KEY);
        push.connect();

        chan = push.subscribe(chanName);

        chan.bind(startEventName, reservationStartedListener);
        chan.bind(endEventName, reservationEndedListener);
    }


    private SubscriptionEventListener reservationStartedListener = new SubscriptionEventListener() {
        @Override
        public void onEvent(String channelName, String eventName, String data) {
            Notifications.notifyReservationStarted(getApplication(), data);
        }
    };

    private SubscriptionEventListener reservationEndedListener = new SubscriptionEventListener() {
        @Override
        public void onEvent(String channelName, String eventName, String data) {
            Notifications.notifyReservationEnded(getApplication(), data);
        }
    };

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
