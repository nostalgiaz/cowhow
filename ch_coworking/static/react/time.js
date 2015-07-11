var TimePicker = React.createClass({
  componentDidMount: function () {
    $(".timepicker").timepicker({
      showInputs: false
    })
    //.on('changeTime.timepicker', function (e) {
    //console.log('The time is ' + e.time.value);
    //console.log('The hour is ' + e.time.hour);
    //console.log('The minute is ' + e.time.minute);
    //console.log('The meridian is ' + e.time.meridian);
    //Action.time(e)
    //});
  },

  componentWillUnmount: function () {
    $(this.getDOMNode()).remove()
  },

  render: function () {
    return <div className="input-append bootstrap-timepicker">
      <div className="input-group">
        <input type="text" className="form-control timepicker"/>
        <div className="input-group-addon">
          <i className="fa fa-clock-o"></i>
        </div>
      </div>
    </div>;
  }
});

