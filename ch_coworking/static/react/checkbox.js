var Checkbox = React.createClass({
  onChange: function (event) {
    Action.checkbox({
      filter: this.props.label,
      checked: event.target.checked
    });
  },

  render: function () {
    var style = {
      'opacity': this.props.checked ? 1 : 0.5
    };
    return <div className="text-center">
      <label style={style}>
        <img src={'/static/imgs/' + this.props.id + '.png'} alt="" width="50" />
        <input type="checkbox" checked={this.props.checked} onChange={this.onChange} style={{display: 'none'}}/>
        <br/>{this.props.label}
      </label>
    </div>;
  }
});
