var Coworkings = React.createClass({
  render: function () {
    if (_.isEmpty(this.props.coworkings))
      return false;

    return <ul>
      {_.map(this.props.coworkings, function (coworking) {
        return <li>{coworking.name} -- {coworking.location.latitude} / {coworking.location.longitude}</li>;
      })}
    </ul>;
  }
});
