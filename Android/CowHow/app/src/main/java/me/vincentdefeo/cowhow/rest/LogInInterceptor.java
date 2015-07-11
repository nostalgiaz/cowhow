package me.vincentdefeo.cowhow.rest;

import android.content.Context;
import android.util.Base64;

import me.vincentdefeo.cowhow.utils.Preferences;
import retrofit.RequestInterceptor;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class LogInInterceptor implements RequestInterceptor {

    private final Context context;

    public LogInInterceptor(Context context)
    {
        this.context = context;
    }

    @Override
    public void intercept(RequestFacade request) {
        final String authVal = Preferences.getUserAuth(context);

        if (authVal != "" && authVal != null) {
            request.addHeader("Authorization", authVal);
        }
    }
}
