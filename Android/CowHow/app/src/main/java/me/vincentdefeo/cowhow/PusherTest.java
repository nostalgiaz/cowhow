package me.vincentdefeo.cowhow;

import android.app.AlertDialog;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.pusher.client.Pusher;
import com.pusher.client.channel.Channel;
import com.pusher.client.channel.SubscriptionEventListener;
import com.pusher.client.connection.ConnectionEventListener;
import com.pusher.client.connection.ConnectionState;
import com.pusher.client.connection.ConnectionStateChange;


public class PusherTest extends AppCompatActivity {

    private TextView pusherTest;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pusher_test);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_pusher_test, menu);

        pusherTest = (TextView) findViewById(R.id.puser_text);

        Pusher p = new Pusher("45656fd4d10dc8df4bdc");
        p.connect(new ConnectionEventListener() {
            @Override
            public void onConnectionStateChange(ConnectionStateChange connectionStateChange) {
                new AlertDialog.Builder(PusherTest.this)
                        .setMessage("RECEIVED")
                        .create().show();
            }

            @Override
            public void onError(String s, String s1, Exception e) {
                new AlertDialog.Builder(PusherTest.this)
                        .setMessage("ERROR")
                        .create().show();
            }
        }, ConnectionState.ALL);

        Channel c = p.subscribe("my-channel");

        c.bind("my-event", new SubscriptionEventListener() {
            @Override
            public void onEvent(String s, String s1, String s2) {
                new AlertDialog.Builder(PusherTest.this).setMessage("EVENT").create().show();
            }
        });

        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
