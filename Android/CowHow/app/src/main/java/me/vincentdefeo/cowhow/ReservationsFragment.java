package me.vincentdefeo.cowhow;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

import me.vincentdefeo.cowhow.async.SimpleAsync;
import me.vincentdefeo.cowhow.rest.CowHowService;
import me.vincentdefeo.cowhow.rest.Reservation;
import me.vincentdefeo.cowhow.utils.Maps;

/**
 * Created by ghzmdr on 12/07/15.
 */
public class ReservationsFragment extends Fragment {

    private RecyclerView list;


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        View v = inflater.inflate(R.layout.fragment_reservations, container, false);

        list = (RecyclerView) v.findViewById(R.id.reservations_list);
        list.setLayoutManager(new LinearLayoutManager(getActivity()));

        new SimpleAsync()
        {
            List<Reservation> reservations = null;

            @Override
            protected void run()
            {
                CowHowService chs = ((CowHowApplication) getActivity().getApplication()).getRestService();
                reservations = chs.getReservations();
            }

            @Override
            protected void then()
            {
                list.setAdapter(new ReservationsAdapter(reservations));
            }

        }.execute();

        return v;
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
            View v = LayoutInflater.from(getActivity())
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
            holder.position.setText(Maps.getAddressFromCoords(getActivity(), current.lat, current.lng));

            holder.root.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent i = new Intent(getActivity(), DetailActivity.class);
                    i.putExtra(DetailActivity.EXTRA, current.pk);
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
