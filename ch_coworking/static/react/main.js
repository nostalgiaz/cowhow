var Main = React.createClass({
  mixins: [Reflux.connect(Store, 'datum')],

  componentDidMount: function () {
    Action.load();
  },

  render: function () {
    return <div className="content" style={{paddingTop: 0, paddingBottom: 0, paddingRight: 0}}>
      <div className="row">
        <div className="col-md-6">
          <Checkboxes filters={this.state.datum.filters.amenities} />
          <hr/>
          <Coworkings coworkings={this.state.datum.coworkings} />
        </div>
        <div className="col-md-6">
          <Map {...this.props} />
        </div>
      </div>
    </div>;
  }
});
