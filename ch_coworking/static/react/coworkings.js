var Coworkings = React.createClass({
  render: function () {
    if (_.isEmpty(this.props.coworkings))
      return false;

    return <div>
      {_.map(this.props.coworkings, function (coworking) {
        console.log(coworking)
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
              <tr>
                <th>Name</th>
                <th>Price</th>
                <th style={{width: "40px"}}>Book!</th>
              </tr>
              {_.map(coworking.tables, function (table) {
                return <tr>
                  <td>{table.name}</td>
                  <td>{table.price}€</td>
                  <td><a className="btn btn-default" href=""><strong>&#8594;</strong></a></td>
                </tr>;
              })}
            </table>
          </div>
        </div>;
      })}
    </div>;
  }
});
