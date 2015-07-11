package me.vincentdefeo.cowhow;

import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import me.vincentdefeo.cowhow.rest.Reservation;
import me.vincentdefeo.cowhow.utils.Maps;


public class DetailActivity extends AppCompatActivity {

    public static final String EXTRA = "EXTRA_RESERVATION";

    ImageView mapImage;
    TextView addressTv, dateTV, hourTv;
    Reservation res;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        mapImage = (ImageView) findViewById(R.id.maps_view);
        addressTv = (TextView) findViewById(R.id.address);
        dateTV = (TextView) findViewById(R.id.date);
        hourTv = (TextView) findViewById(R.id.hour);

        res = (Reservation) getIntent().getExtras().getSerializable(EXTRA);

        addressTv.setText(Maps.getAddressFromCoords(this, res.lat, res.lng));
        dateTV.setText(res.date);
        hourTv.setText(res.fromHour);

        Maps.getMapImage(this, res.lat, res.lng, mapImage);

        mapImage.setOnClickListener(openMapOnClick);
        addressTv.setOnClickListener(openMapOnClick);
    }

    private View.OnClickListener openMapOnClick = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            String geoUri = "http://maps.google.com/maps?q=loc:" + res.lat + "," + res.lng + " (" + addressTv.getText() + ")";
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(geoUri));
            startActivity(intent);
        }
    };
}
