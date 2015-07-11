var Map = React.createClass({
  componentDidMount: function () {
    L.mapbox.accessToken = this.props.accessToken;
    var map = L.mapbox.map('map', 'mapbox.streets');
  },

  render: function () {
    return <div id="map"></div>;
  }
});

