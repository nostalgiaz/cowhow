var Main = React.createClass({
  mixins: [Reflux.connect(Store, 'datum')],

  componentDidMount: function () {
    Action.load();
  },

  render: function () {
    return <div className="content" style={{paddingTop: 0, paddingBottom: 0, paddingRight: 0}}>
      <div className="row">
        <div className="col-md-6">
          <div className="content" style={{ overflow: 'scroll', height: 'calc(100vh - 50px)', position: 'absolute' }}>
            <div className="row">
              <div className="col-md-6">
                <DatePicker />
              </div>
              <div className="col-md-6">
                <TimePicker />
              </div>
            </div>
            <br/>
            <Checkboxes filters={this.state.datum.filters.amenities} />
            <hr/>
            <Coworkings coworkings={this.state.datum.coworkings} />
          </div>
        </div>
        <div className="col-md-6">
          <Map {...this.props} coworkings={this.state.datum.coworkings} />
        </div>
      </div>
    </div>;
  }
});
