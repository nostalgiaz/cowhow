package me.vincentdefeo.cowhow;

import android.app.Application;
import android.content.Intent;

import me.vincentdefeo.cowhow.rest.CowHowService;
import me.vincentdefeo.cowhow.rest.LogInInterceptor;
import retrofit.RequestInterceptor;
import retrofit.RestAdapter;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class CowHowApplication extends Application {

    private static final String API_ENDPOINT = "http://10.1.2.109:8000";

    @Override
    public void onCreate() {
        super.onCreate();
        startService(new Intent(this, PusherService.class));
    }

    public CowHowService getRestService()
    {
        RequestInterceptor ri = new LogInInterceptor(this);

        return new RestAdapter.Builder()
                .setRequestInterceptor(ri)
                .setLogLevel(RestAdapter.LogLevel.BASIC)
                .setEndpoint(API_ENDPOINT)
                .build()
                .create(CowHowService.class);
    }
}
