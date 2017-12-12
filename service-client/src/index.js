import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import TimeSeriesChart from './components/TimeSeriesChart/chart'


const height = 300
const width = 800
const margins = {top: 20, right: 20, bottom: 60, left: 40}

class App extends Component {
  constructor() {
    super()
    this.state = {
      commits: [],
      commits_loading: true
    }
  }
  
  componentDidMount() {
    this.getUsers();
  }
  
  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/daily_commits`)
    .then((res) => {
      // process data
      let data = res.data
      data.map((d,i) => {
        d.date = new Date(d.date)
        return d
      })
      this.setState({ commits: data, commits_loading: false })
    })
    .catch((err) => { console.log(err); })
  }

  // {!commits_loading && <TimeSeriesChart data={commits} height={height} width={width} margin={margin}/>}

  render() {
    const { commits, commits_loading } = this.state
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <br/>
            <h1>Header</h1>
            <hr/><br/>
              <div>
                {!commits_loading && <TimeSeriesChart data={commits} width={width} height={height} margins={margins} />}
              </div>
          </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);