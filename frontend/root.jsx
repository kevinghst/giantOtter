import React from 'react';
import ReactDOM from 'react-dom';
import List from './list';

import data from './data.json';

class Root extends React.Component {
  render() {
    return(
      <div>
        <List data = {data} />
      </div>
    );
  }
}

document.addEventListener('DOMContentLoaded', () => {
  ReactDOM.render(<Root/>, document.getElementById('main'));
});
