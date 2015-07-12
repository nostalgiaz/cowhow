var Coworkings = React.createClass({
  onClick: function (tablePk) {
    Action.pay(tablePk);
  },

  render: function () {
    var that = this;

    if (_.isEmpty(this.props.coworkings))
      return false;

    return <div>
      {_.map(this.props.coworkings, function (coworking) {
        return <div className="box box-success" style={{borderTopColor: '#E6A4FA'}}>
          <div className="box-header ui-sortable-handle">
            <h3 className="box-title">{coworking.name}</h3>
          </div>
          <div className="box-body chat">
            <img src={'/static/imgs/coffee.png'} alt="" width="30" style={{marginRight: '5px', opacity: coworking.amenities.indexOf('coffee') >= 0 ? 1 : 0.5 }} />
            <img src={'/static/imgs/students.png'} alt="" width="30" style={{marginRight: '5px', opacity: coworking.amenities.indexOf('students') >= 0 ? 1 : 0.5 }} />
            <img src={'/static/imgs/axe.png'} alt="" width="30" style={{marginRight: '5px', opacity: coworking.amenities.indexOf('axe') >= 0 ? 1 : 0.5 }} />
            <hr/>
            <table className="table">
              <tbody>
              <tr>
                <th>Name</th>
                <th>Price</th>
                <th style={{width: "40px"}}>Book!</th>
              </tr>
              {_.map(coworking.tables, function (table) {
                return <tr>
                  <td>{table.name}</td>
                  <td>{table.price}€</td>
                  <td><span className="btn btn-default" onClick={function () {that.onClick(table.pk)}}><strong>&#8594;</strong></span></td>
                </tr>;
              })}
                </tbody>
            </table>
          </div>
        </div>;
      })}
    </div>;
  }
});
