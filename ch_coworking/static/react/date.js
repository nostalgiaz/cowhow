var DatePicker = React.createClass({
  componentDidMount: function () {
    $(this.getDOMNode()).datepicker({
       autoclose: true,
      todayHighlight: true
    }).on('changeDate', function (e) {
      console.log(e)
      Action.date(e)
    });
  },

  componentWillUnmount: function () {
    $(this.getDOMNode()).remove()
  },

  render: function () {
    return <input type="text" type="text" className="form-control"/>;
  }
});

