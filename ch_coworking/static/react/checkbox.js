var Checkbox = React.createClass({
  onChange: function (event) {
    Action.checkbox({
      filter: this.props.label,
      checked: event.target.checked
    });
  },

  render: function () {
    return <label><input type="checkbox" checked={this.props.checked} onChange={this.onChange} /> {this.props.label}</label>;
  }
});
