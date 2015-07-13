package me.vincentdefeo.cowhow.rest;

import com.google.gson.annotations.Expose;

import java.util.List;

/**
 * Created by ghzmdr on 12/07/15.
 */
public class CoworkingResults {

    @Expose
    public List<Coworking> results;

    public class Coworking {
        @Expose
        public String name;

        @Expose
        public String amenities[];

        @Expose
        public String photos[];

        @Expose
        public JsonLocation location;

        public class JsonLocation {
            @Expose
            public String latitude;
            @Expose
            public String longitude;
        }
    }
}