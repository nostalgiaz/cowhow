package me.vincentdefeo.cowhow;

import android.location.Geocoder;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;

import java.io.IOException;
import java.util.List;

import me.vincentdefeo.cowhow.async.SimpleAsync;
import me.vincentdefeo.cowhow.rest.CowHowService;
import me.vincentdefeo.cowhow.rest.Reservation;
import me.vincentdefeo.cowhow.utils.Preferences;


public class MainActivity extends AppCompatActivity {

    // private Fragment[] fragments = {new SearchFragment(), new ReservationsFragment() };

    private FrameLayout fragmentContainer;
    private String actionBarTitle = "";

    private RecyclerView list;
    private Toolbar toolbar;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //fragmentContainer = (FrameLayout) findViewById(R.id.fragment_container);

        toolbar = (Toolbar) findViewById(R.id.toolbar);
        //setSupportActionBar(toolbar);

        list = (RecyclerView) findViewById(R.id.reservations_list);



        new SimpleAsync()
        {
            List<Reservation> reservations = null;

            @Override
            protected void run()
            {
                CowHowService chs = ((CowHowApplication) getApplication()).getRestService();
                reservations = chs.getReservations();//Preferences.getUserName(getBaseContext()));
            }

            protected void then()
            {
                list.setAdapter(new ReservationsAdapter(reservations));
            }
        }.execute();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);

        return super.onCreateOptionsMenu(menu);
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

    private class ReservationViewHolder extends RecyclerView.ViewHolder
    {
        View root;

        TextView position;
        TextView date;
        TextView hour;

        public ReservationViewHolder(View itemView) {
            super(itemView);
            root = itemView;

            position = (TextView) itemView.findViewById(R.id.location);
            date = (TextView) itemView.findViewById(R.id.date);
            hour = (TextView) itemView.findViewById(R.id.hour);
        }
    }

    private class ReservationsAdapter extends RecyclerView.Adapter<ReservationViewHolder>
    {

        private final List<Reservation> reservations;

        ReservationsAdapter(List<Reservation> reservations)
        {
            this.reservations = reservations;
        }

        @Override
        public ReservationViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View v = new View(getBaseContext());
            v.inflate(getBaseContext(), R.layout.reservation_list_item, null);

            return new ReservationViewHolder(v);
        }

        @Override
        public void onBindViewHolder(ReservationViewHolder holder, int position)
        {
            Reservation current = reservations.get(position);

            String address = null;
            Geocoder g = new Geocoder(getBaseContext());

            try {
                address = g.getFromLocation(current.lat, current.lng, 1).get(0).getAddressLine(0);
            } catch (IOException e) {
                e.printStackTrace();
                address = current.lat + " " + current.lng;
            }

            holder.date.setText(current.date);
            holder.hour.setText(current.fromHour);
            holder.position.setText(address);
        }

        @Override
        public int getItemCount() {
            return reservations.size();
        }
    }
}
