package me.vincentdefeo.cowhow;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

/**
 * Created by ghzmdr on 11/07/15.
 */
public class SearchFragment extends Fragment {

    private RecyclerView list;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_search, container);

        list = (RecyclerView) v.findViewById(R.id.reservations_list);

        return v;
    }


}
