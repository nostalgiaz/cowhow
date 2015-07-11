var Checkboxes = React.createClass({
  render: function () {
    return <div className="row">
      {_.map(this.props.filters, function (filter) {
        return <div className="col-md-3">
          <Checkbox label={filter.label} checked={filter.checked} />
        </div>
      })}
    </div>;
  }
});
