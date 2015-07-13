package me.vincentdefeo.cowhow;

import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import com.google.android.gms.maps.SupportMapFragment;


public class MainActivity extends AppCompatActivity {

    private Fragment[] fragments = {new CoworkSearchFragment(), new ReservationsFragment() };

    private String actionBarTitle = "";

    private Toolbar toolbar;

    private TabLayout tabs;
    private ViewPager pager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setTitle("");
        tabs = (TabLayout) findViewById(R.id.tabs);


        pager = (ViewPager) findViewById(R.id.fragment_pager);
        setSupportActionBar(toolbar);

        pager.setAdapter(new MainPagerAdapter(getSupportFragmentManager()));
        tabs.setupWithViewPager(pager);

        tabs.getTabAt(0).setIcon(R.drawable.ic_map_grey600_24dp);
        tabs.getTabAt(1).setIcon(R.drawable.ic_briefcase_grey600_24dp);
    }

    private class MainPagerAdapter extends FragmentPagerAdapter {

        public MainPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public int getCount() {
            return fragments.length;
        }

        @Override
        public Fragment getItem(int position) {
            return fragments[position];
        }
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
        if (id == R.id.action_filters) {
            return true;
        }

        if (id == R.id.action_location) {
            ((CoworkSearchFragment)fragments[0]).updatePosition();

            return true;
        }
/*
        if (id == R.id.action_search) {
            return true;
        }
*/
        return super.onOptionsItemSelected(item);
    }
}
