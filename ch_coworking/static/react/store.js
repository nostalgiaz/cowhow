var Store = Reflux.createStore({
  listenables: [Action],

  onLoad: function () {
    this.updateFilters();
  },

  onPay: function (table) {
    $.post('/api/me/credit-cards/', {'nonce': 'fake-valid-nonce'}, function (data) {
      var token = data.token;
      $.post('/api/reservations/', {
        'table': table,
        'date': new Date().toISOString().slice(0,10),
        'from_hour': '13:00',
        'to_hour': '15:00',
        'payment_token': token
      }, function () {
        alert('Yay! The table is yours!')
      })
    })
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
    this.datum.filters.top_left = event._northEast.lat + ',' + event._southWest.lng;
    this.datum.filters.bottom_right = event._southWest.lat + ',' + event._northEast.lng;
    this.updateFilters();
  },

  updateFilters: function () {
    var that = this;
    $.ajax('/api/coworkings/', {
      data: {
        amenities: _.map(_.filter(this.datum.filters.amenities, function (filter) {
          return filter.checked;
        }), function (filter) {
          return filter.label;
        }),
        top_left: this.datum.filters.top_left,
        bottom_right: this.datum.filters.bottom_right
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
          {id: 'coffee', label: 'coffee', checked: false},
          {id: 'students', label: 'students', checked: false},
          {id: 'axe', label: 'battle axe', checked: false}
        ],
        top_left: '',
        bottom_right: ''
      },
      coworkings: []
    };
    return this.datum;
  }
});
