import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import axios from 'axios'
import TimeSeriesChart from './components/TimeSeriesChart/chart'
import SummaryTable from './components/SummaryTable/Table'

const height = 300
const width = 800
const plot_margins = {top: 20, right: 20, bottom: 60, left: 40}
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
  
  componentDidMount() {
    this.getSummaryTable()
  }

  getSummaryTable() {
    axios.all([
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/summary_table`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_commits`),
      axios.get(`${process.env.REACT_APP_GIT_SERVICE_URL}/daily_devs`)
    ])
    .then(axios.spread((r_summary, r_commits, r_devs) => {
      // process data
      let summary = r_summary.data
      let commits = r_commits.data
      let devs = r_devs.data
      
      // process commits
      commits.map((d,i) => {
        d.date = new Date(d.date)
        return d
      })
      
      // create sparklines for commits
      let _s_commits = commits.slice(commits.length - sparkline_days)
      summary.map((d,i) => {
        d['sparkline_commits'] = _s_commits.map(s => s[d.ticker])
      })

      // create sparklines for devs
      let _s_devs = devs.slice(devs.length - sparkline_days)
      summary.map((d,i) => {
        d['sparkline_devs'] = _s_devs.map(s => s[d.ticker])
      })

      // merge today_commits with change
      summary.map(d => {
        d['today_commits_merged']=`${d.today_commits.toFixed(2)} (${d.today_commits_change > 0 ? '+': ''}${d.today_commits_change.toFixed(2)}%)`
      })

      // merge daily_devs with change
      summary.map(d => {
        d['today_devs_merged']=`${d.today_devs.toFixed(2)} (${d.today_devs_change > 0 ? '+': ''}${d.today_devs_change.toFixed(2)}%)`
      })

      // merge contributors with ratio
      summary.map(d => {
        d['developers']=`${d.unique_contributors} (${d.developers_ratio.toFixed(2)}% > 5)`
      })

      // export variables
      this.setState({ summary_table: summary, summary_table_loading: false })
      this.setState({ commits: commits, commits_loading: false })
    }))
    .catch((err) => { console.log(err); })
  }

  render() {
    const { commits, commits_loading, commits_graph } = this.state
    const { summary_table, summary_table_loading } = this.state
    return (
      <div className="container">
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
              margins={plot_margins} />}
          </div>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);