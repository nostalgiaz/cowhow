package me.vincentdefeo.cowhow.utils;

import android.content.Context;
import android.content.SharedPreferences;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class Preferences {

    public static final String PREFS_AUTH_FILE = "AUTH_FILE";
    public static final String PREFS_AUTH_USER= "AUTH_USER";
    public static final String PREFS_AUTH_PWD= "AUTH_PWD";

    public static SharedPreferences getPreferenceFile(Context context, String name)
    {
        return context.getSharedPreferences(name, 0);
    }

    public static void putString(Context context, String name, String key, String value)
    {
        SharedPreferences.Editor editor = getPreferenceFile(context, name).edit();
        editor.putString(key, value);
        editor.commit();
    }

    public static String getString(Context context, String name, String key)
    {
        return getPreferenceFile(context, name).getString(key, "");
    }

    public static void saveUser(Context c, String name, String pwd)
    {
        putString(c, PREFS_AUTH_FILE, PREFS_AUTH_USER, name);
        putString(c, PREFS_AUTH_FILE, PREFS_AUTH_PWD, pwd);
    }

    public static String getUserAuth(Context c)
    {
        return getString(c, PREFS_AUTH_FILE, PREFS_AUTH_USER) + ":" +  getString(c, PREFS_AUTH_FILE, PREFS_AUTH_PWD);
    }

    public static String getUserName(Context c)
    {
        return getString(c, PREFS_AUTH_FILE, PREFS_AUTH_USER);
    }
}

