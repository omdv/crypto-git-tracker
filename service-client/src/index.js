import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import TimeSeriesChart from './components/TimeSeriesChart/chart'
import SummaryTable from './components/SummaryTable/Table'

const height = 300
const width = 800
const margins = {top: 20, right: 20, bottom: 60, left: 40}
const sparkline_days = 60

class App extends Component {
  constructor() {
    super()
    this.state = {
      commits: [],
      commits_loading: true,
      summary_table: [],
      summary_table_loading: true,
    }
  }

  getCommits() {
    axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_commits`)
  }

  getSummary() {
    axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/summary_table`)
  }

  getDevs() {
    axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_devs`)
  }
  
  componentDidMount() {
    // this.getCommits()
    this.getSummaryTable()
  }
  



  getCommits() {
    axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_commits`)
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

  getSummaryTable() {
    axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/summary_table`)
    .then((response_summary) => {
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_commits`)
      .then((response_commits) => {
        // process data
        let summary = response_summary.data
        let commits = response_commits.data
        
        // process commits
        commits.map((d,i) => {
          d.date = new Date(d.date)
          return d
        })
        
        // create sparklines
        let sparklines = commits.slice(commits.length - sparkline_days)
        summary.map((d,i) => {
          d['sparkline'] = sparklines.map(s => s[d.coin])
        })

        // merge daily_commits with change
        summary.map(d => {
          d['daily_commits']=`${d.daily_commits_last.toFixed(2)} (${d.daily_commits_change > 0 ? '+': ''}${d.daily_commits_change.toFixed(2)}%)`
        })

        // merge contributors with ratio
        summary.map(d => {
          d['developers']=`${d.unique_contributors} (${d.developers_ratio.toFixed(2)}% > 5)`
        })

        // export variables
        this.setState({ summary_table: summary, summary_table_loading: false })
        this.setState({ commits: commits, commits_loading: false })
      })
      .catch((err) => { console.log(err); })
    })
    .catch((err) => { console.log(err); })
  }

  render() {
    const { commits, commits_loading } = this.state
    const { summary_table, summary_table_loading } = this.state
    return (
      <div className="container">
          <div className="col-md-6">
            <br/>
            <h1>Header</h1>
            <hr/><br/>
          </div>
          <div className="col-md-12">
            <SummaryTable
              data={summary_table}
              loading={summary_table_loading} />
          </div>
          <div className="col-md-6">  
            {!commits_loading && <TimeSeriesChart
              data={commits}
              width={width}
              height={height}
              margins={margins} />}
          </div>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);