var Map = React.createClass({
  componentDidMount: function () {
    var that = this;

    L.mapbox.accessToken = this.props.accessToken;
    this.map = L.mapbox.map('map', 'mapbox.streets', {
      maxZoom: 15
    });
    this.map.locate();

    this.myLayer = L.mapbox.featureLayer().addTo(this.map);


    this.map.on('moveend', function (move) {
      Action.map(that.map.getBounds());
    });

    this.map.on('locationfound', function (e) {
      that.map.fitBounds(e.bounds);

      that.myLayer.setGeoJSON({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [e.latlng.lng, e.latlng.lat]
        },
        properties: {
          'title': 'Here I am!',
          'marker-color': '#ff8888',
          'marker-symbol': 'star'
        }
      });
    });
  },

  componentWillReceiveProps: function (props) {
    var that = this;
    _.each(props.coworkings, function (coworking) {
      L.marker([50.5, 30.5]).addTo(that.map);
    });


  },

  componentWillUnmount: function () {
    this.map.remove()
  },

  render: function () {
    return <div id="map"></div>;
  }
});

