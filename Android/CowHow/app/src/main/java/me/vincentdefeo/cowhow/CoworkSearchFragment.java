package me.vincentdefeo.cowhow;

import android.content.Intent;
import android.location.Location;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.*;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import me.vincentdefeo.cowhow.async.SimpleAsync;
import me.vincentdefeo.cowhow.rest.CoworkingResults;
import me.vincentdefeo.cowhow.utils.REST;

/**
 * Created by ghzmdr on 12/07/15.
 */
public class CoworkSearchFragment extends SupportMapFragment implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener{

    private GoogleApiClient gApi;
    private List<CoworkingResults.Coworking> visibleCows;

    Map<Marker, CoworkingResults.Coworking> markerCows;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        buildGoogleApiClient();
        markerCows = new HashMap<>();
        return super.onCreateView(inflater, container, savedInstanceState);
    }

    protected synchronized void buildGoogleApiClient() {
        gApi = new GoogleApiClient.Builder(getActivity())
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();
        gApi.connect();
    }

    public void updatePosition() {
        Location location = LocationServices.FusedLocationApi.getLastLocation(gApi);

        if (location != null) {
            getMap().moveCamera(CameraUpdateFactory.newLatLng(new LatLng(location.getLatitude(), location.getLongitude())));
            getMap().moveCamera(CameraUpdateFactory.zoomTo(10));
        }

        new SimpleAsync()
        {
            List<CoworkingResults.Coworking> cows;
            LatLngBounds bounds = getMap().getProjection().getVisibleRegion().latLngBounds;

            @Override
            protected void run() {
                cows = REST.getCoworkingsInBounds(
                                getActivity().getApplication(),
                                bounds
                        );
            }

            @Override
            protected void then() {

                for (CoworkingResults.Coworking c : cows) {
                    Marker m = setMarker(c.location, c.name);
                    markerCows.put(m, c);
                }


            }
        }.execute();
    }

    private Marker setMarker(CoworkingResults.Coworking.JsonLocation location, String name) {
        MarkerOptions mO = new MarkerOptions()
                .position(new LatLng(Double.parseDouble(location.latitude), Double.parseDouble(location.longitude)))
                .title(name)
                .flat(true);

        Marker marker = getMap().addMarker(mO);
        return marker;
    }



    @Override
    public void onConnected(Bundle bundle) {
        updatePosition();
        getMap().setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener() {
            @Override
            public void onInfoWindowClick(Marker marker) {
                CoworkingResults.Coworking cow = markerCows.get(marker);
                Intent i = new Intent(getActivity(), CoworkingDetail.class);
                i.putExtra(CoworkingDetail.EXTRA, cow.pk);
                startActivity(i);
            }
        });
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {

    }
}
