var DatePicker = React.createClass({
  componentDidMount: function () {
    $(this.getDOMNode()).find('input').datepicker({
       autoclose: true,
      todayHighlight: true
    }).on('changeDate', function (e) {
      Action.date(e)
    });
  },

  componentWillUnmount: function () {
    $(this.getDOMNode()).remove()
  },

  render: function () {
    return <div>
      <strong>Date:</strong><br/>
      <input type="text" type="text" className="form-control"/>
    </div>;
  }
});

