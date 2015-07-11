package me.vincentdefeo.cowhow;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;

import com.pusher.client.Pusher;

import java.util.List;

import me.vincentdefeo.cowhow.async.SimpleAsync;
import me.vincentdefeo.cowhow.rest.CowHowService;
import me.vincentdefeo.cowhow.rest.Reservation;
import me.vincentdefeo.cowhow.utils.Maps;


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

        //toolbar = (Toolbar) findViewById(R.id.toolbar);
        //setSupportActionBar(toolbar);

        list = (RecyclerView) findViewById(R.id.reservations_list);
        list.setLayoutManager(new LinearLayoutManager(this));

        new SimpleAsync()
        {
            List<Reservation> reservations = null;

            @Override
            protected void run()
            {
                CowHowService chs = ((CowHowApplication) getApplication()).getRestService();
                reservations = chs.getReservations();
            }

            @Override
            protected void then()
            {
                list.setAdapter(new ReservationsAdapter(reservations));
            }

        }.execute();

        findViewById(R.id.puser_btn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, PusherTest.class));
            }
        });
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
        public ReservationViewHolder onCreateViewHolder(ViewGroup parent, int viewType)
        {
            View v = LayoutInflater.from(MainActivity.this)
                        .inflate(R.layout.reservation_list_item, parent, false);

            return new ReservationViewHolder(v);
        }

        @Override
        public void onBindViewHolder(ReservationViewHolder holder, int position)
        {
            final Reservation current = reservations.get(position);



            holder.date.setText(current.date);
            holder.date.setText(current.date);
            holder.hour.setText(current.fromHour);
            holder.position.setText(Maps.getAddressFromCoords(MainActivity.this, current.lat, current.lng));

            holder.root.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent i = new Intent(MainActivity.this, DetailActivity.class);

                    Bundle b = new Bundle();
                    b.putSerializable(DetailActivity.EXTRA, current);
                    i.putExtras(b);

                    startActivity(i);
                }
            });
        }

        @Override
        public int getItemCount()
        {
            return reservations.size();
        }
    }
}
