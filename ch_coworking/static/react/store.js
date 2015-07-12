var Store = Reflux.createStore({
  listenables: [Action],

  onLoad: function () {
    this.updateFilters();
  },

  onCheckbox: function (event) {
    this.datum.filters.amenities = _.map(this.datum.filters.amenities, function (amenity) {
      if (event.filter === amenity.label)
        amenity.checked = event.checked;
      return amenity;
    });
    this.updateFilters();
  },

  onDate: function (event) {

  },

  onTime: function (event) {

  },

  onMap: function (event) {
console.log(event)
  },

  updateFilters: function () {
    var that = this;
    $.ajax('/api/coworkings/', {
      data: {
        amenities: _.map(_.filter(this.datum.filters.amenities, function (filter) {
          return filter.checked;
        }), function (filter) {
          return filter.label;
        })
      },
      'type': 'GET'
    }).done(function (data) {
      that.datum.coworkings = data.results;
      that.trigger(that.datum);
    });
  },

  getInitialState: function () {
    this.datum = {
      filters: {
        amenities: [
          {label: 'caffe', checked: false},
          {label: 'ethernet', checked: false},
          {label: 'meetingRoom', checked: false},
          {label: 'battleAxe', checked: false}
        ],
        top_left: ''
      },
      coworkings: []
    };
    return this.datum;
  }
});
