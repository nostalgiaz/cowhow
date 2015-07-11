package me.vincentdefeo.cowhow.async;

import android.os.AsyncTask;

/**
 * Created by ghzmdr on 11/07/15.
 */
public abstract class SimpleAsync extends AsyncTask<Void, Void, Void> {

    protected void prepare(){}
    protected abstract void run();
    protected abstract void then();


    @Override
    protected Void doInBackground(Void... params) {
        run();
        return null;
    }

    @Override
    protected void onPreExecute() {
        prepare();
    }

    @Override
    protected void onPostExecute(Void aVoid) {
        then();
    }
}
