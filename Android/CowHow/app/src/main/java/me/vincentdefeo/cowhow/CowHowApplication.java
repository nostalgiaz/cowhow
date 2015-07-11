package me.vincentdefeo.cowhow;

import android.app.Application;

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
    }

    public CowHowService getRestService()
    {
        RequestInterceptor ri = new LogInInterceptor(this);

        return new RestAdapter.Builder()
                .setRequestInterceptor(ri)
                .setEndpoint(API_ENDPOINT)
                .build()
                .create(CowHowService.class);
    }
}
